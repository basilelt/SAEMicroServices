#api_common/urls.py
from django.urls import path
from .views import BookingCreateView, BookingListView, BookingDetailView, SeatCheckView, BookingValidationView, PaymentValidationView

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='create_booking'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('check-seats/<int:flight_id>/', SeatCheckView.as_view(), name='check_seats'),
    path('validate-booking/<int:booking_id>/', BookingValidationView.as_view(), name='validate_booking'),
    path('validate-payment/', PaymentValidationView.as_view(), name='validate_payment'),
]
