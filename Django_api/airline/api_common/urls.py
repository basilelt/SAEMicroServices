#api_common/urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserListView, UserDetailView, FlightListView,
    FlightDetailView, BookingListView, BookingDetailView, AirportListView,
    AirportDetailView, PlaneListView, PlaneDetailView, AllBookingsListView,
    AddFlightView, UpdateFlightView, DeleteFlightView, AddAirportView,
    UpdateAirportView, DeleteAirportView, AddPlaneView, UpdatePlaneView, DeletePlaneView,
    TransactionListView, TransactionDetailView, TrackCreateView,
    CancellationRequestListView, CancellationRequestDetailView, PaymentGatewayListView, PaymentGatewayDetailView
)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
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

    # new
    path('tracks/add/', TrackCreateView.as_view(), name='add-track'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('cancellation-requests/', CancellationRequestListView.as_view(), name='cancellation-request-list'),
    path('cancellation-requests/<int:pk>/', CancellationRequestDetailView.as_view(), name='cancellation-request-detail'),
    path('payment-gateways/', PaymentGatewayListView.as_view(), name='payment-gateway-list'),
    path('payment-gateways/<int:pk>/', PaymentGatewayDetailView.as_view(), name='payment-gateway-detail'),
]
