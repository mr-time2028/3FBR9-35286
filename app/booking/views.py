from drf_spectacular.utils import extend_schema

from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import (
    Booking,
    Table,
    Person,
    Seat,
)
from .serializers import (
    SeatSerializer,
    BookingSerializer,
    CancelBookingSerializer,
)


class BookingAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return []

    def get(self, request, *args, **kwargs):
        available_seats = Seat.objects.filter(is_reserved=False).select_related('table')
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=BookingSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        persons_data = serializer.validated_data["persons"]
        is_full_table = serializer.validated_data["is_full_table"]
        seat_count = serializer.validated_data.get("seat_count", 0)
        if not seat_count % 2 == 0:
            seat_count += 1

        with transaction.atomic():
            persons = [Person(booker=user, **p) for p in persons_data]

            if is_full_table:
                table_with_n_seats = Table.objects.filter(
                    seat__is_reserved=False
                ).annotate(
                    available_seats=Count('seat')
                ).filter(
                    available_seats=seat_count
                ).order_by('available_seats').first()

                if not table_with_n_seats:
                    return Response({"detail": "no available full table for reservation."},
                                    status=status.HTTP_400_BAD_REQUEST)

                seats = Seat.objects.filter(table=table_with_n_seats)

                total_cost = (table_with_n_seats.seats - 1) * table_with_n_seats.seat_cost
            else:
                seats = Seat.objects.filter(is_reserved=False)[:seat_count]
                if len(seats) < seat_count:
                    return Response(
                        {"detail": f"only {len(seats)} seats are available, cannot reserve {seat_count}."},
                        status=status.HTTP_400_BAD_REQUEST)
                total_cost = sum(seat.table.seat_cost for seat in seats)

            # booking operation with bulk create
            bookings_info = []
            bookings = []

            for seat, person in zip(seats, persons):
                seat.is_reserved = True
                seat.save()

                booking = Booking(person=person, seat=seat)
                bookings.append(booking)

                booking_info = {
                    "booking_id": None,
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "seat_id": seat.id,
                    "table_id": seat.table.id,
                    "cost": seat.cost if not is_full_table else (
                        seat.table.seat_cost if len(seats) == seat.table.seats else seat.table.seat_cost - 1)
                }
                bookings_info.append(booking_info)

            Booking.objects.bulk_create(bookings)

            for booking, booking_info in zip(bookings, bookings_info):
                booking_info["booking_id"] = booking.id

        return Response({
            "message": "Booking successful!",
            "bookings": bookings_info,
            "total_cost": total_cost
        }, status=status.HTTP_201_CREATED)


class CancelBookingAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return []

    @extend_schema(request=CancelBookingSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CancelBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking_id = serializer.validated_data.get('booking_id')

        booking = get_object_or_404(Booking, id=booking_id)

        if booking.is_cancelled:
            return Response({"detail": "this booking has already been canceled."}, status=status.HTTP_400_BAD_REQUEST)

        booking.is_cancelled = True
        booking.save()

        seat = booking.seat
        seat.is_reserved = False
        seat.save()

        return Response({"detail": f"booking {booking_id} has been successfully canceled."}, status=status.HTTP_200_OK)
