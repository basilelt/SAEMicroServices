# api_staff/urls.py
from django.urls import path
from .views import AddFlightView, DeleteFlightView, UpdateFlightView, FlightListView, StaffLoginView, AirportListView, AirportDetailView, PlaneListView, PlaneDetailView, BookingListView

urlpatterns = [
    path('add-flight/', AddFlightView.as_view(), name='add_flight'),
    path('delete-flight/<int:pk>/', DeleteFlightView.as_view(), name='delete_flight'),
    path('update-flight/<int:pk>/', UpdateFlightView.as_view(), name='update_flight'),
    path('flights/', FlightListView.as_view(), name='flight_list'),
    path('login/', StaffLoginView.as_view(), name='staff_login'),
    path('airports/', AirportListView.as_view(), name='airport_list'),
    path('airports/<int:pk>/', AirportDetailView.as_view(), name='airport_detail'),
    path('planes/', PlaneListView.as_view(), name='plane_list'),
    path('planes/<int:pk>/', PlaneDetailView.as_view(), name='plane_detail'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
]
