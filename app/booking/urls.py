from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    path('book/', views.BookingAPIView.as_view(), name='book'),
    path('cancel/', views.CancelBookingAPIView.as_view(), name='cancel_book'),
]
