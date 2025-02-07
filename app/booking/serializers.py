from rest_framework import serializers

from .models import (
    Seat,
    Person,
)


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'table']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name']


class BookingSerializer(serializers.Serializer):
    persons = PersonSerializer(many=True)
    is_full_table = serializers.BooleanField()
    seat_count = serializers.IntegerField()


class CancelBookingSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()
