#api_common/urls.py
from django.urls import path
from .views import (
    UserListView, UserDetailView, FlightListView,
    FlightDetailView, BookingListView, BookingDetailView, AirportListView,
    AirportDetailView, PlaneListView, PlaneDetailView, AllBookingsListView,
    AddFlightView, UpdateFlightView, DeleteFlightView, AddAirportView,
    UpdateAirportView, DeleteAirportView, AddPlaneView, UpdatePlaneView, DeletePlaneView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('flights/', FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('airports/', AirportListView.as_view(), name='airport-list'),
    path('airports/<int:pk>/', AirportDetailView.as_view(), name='airport-detail'),
    path('planes/', PlaneListView.as_view(), name='plane-list'),
    path('planes/<int:pk>/', PlaneDetailView.as_view(), name='plane-detail'),
    path('all-bookings/', AllBookingsListView.as_view(), name='all-bookings-list'),
    path('flights/add/', AddFlightView.as_view(), name='add-flight'),
    path('flights/update/<int:pk>/', UpdateFlightView.as_view(), name='update-flight'),
    path('flights/delete/<int:pk>/', DeleteFlightView.as_view(), name='delete-flight'),
    path('airports/add/', AddAirportView.as_view(), name='add-airport'),
    path('airports/update/<int:pk>/', UpdateAirportView.as_view(), name='update-airport'),
    path('airports/delete/<int:pk>/', DeleteAirportView.as_view(), name='delete-airport'),
    path('planes/add/', AddPlaneView.as_view(), name='add-plane'),
    path('planes/update/<int:pk>/', UpdatePlaneView.as_view(), name='update-plane'),
    path('planes/delete/<int:pk>/', DeletePlaneView.as_view(), name='delete-plane'),
]
