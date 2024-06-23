#api_common/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Gestion des vols
    path('flights/', FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
    path('flights/add/', AddFlightView.as_view(), name='add-flight'),
    path('flights/update/<int:pk>/', UpdateFlightView.as_view(), name='update-flight'),
    path('flights/delete/<int:pk>/', DeleteFlightView.as_view(), name='delete-flight'),

    # Gestion des réservations
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/add/', BookingListView.as_view(), name='add-booking'),  # Utiliser la même vue, ajouter une route
    path('bookings/update/<int:pk>/', BookingDetailView.as_view(), name='update-booking'),  # Utiliser la même vue, ajouter une route
    path('bookings/delete/<int:pk>/', BookingDetailView.as_view(), name='delete-booking'),  # Utiliser la même vue, ajouter une route
    path('bookings/confirm/', ConfirmBookingView.as_view(), name='confirm-booking'),  # new-2

    # Gestion des transactions
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/add/', TransactionListView.as_view(), name='add-transaction'),  # Utiliser la même vue, ajouter une route
    path('transactions/update/<int:pk>/', TransactionDetailView.as_view(), name='update-transaction'),  # Utiliser la même vue, ajouter une route
    path('transactions/delete/<int:pk>/', TransactionDetailView.as_view(), name='delete-transaction'),  # Utiliser la même vue, ajouter une route

    # Gestion des demandes d'annulation
    path('cancellation-requests/', CancellationRequestListView.as_view(), name='cancellation-request-list'),
    path('cancellation-requests/<int:pk>/', CancellationRequestDetailView.as_view(), name='cancellation-request-detail'),
    path('cancellation-requests/add/', CancellationRequestListView.as_view(), name='add-cancellation-request'),  # Utiliser la même vue, ajouter une route
    path('cancellation-requests/update/<int:pk>/', CancellationRequestDetailView.as_view(), name='update-cancellation-request'),  # Utiliser la même vue, ajouter une route
    path('cancellation-requests/delete/<int:pk>/', CancellationRequestDetailView.as_view(), name='delete-cancellation-request'),  # Utiliser la même vue, ajouter une route

    # Gestion des passerelles de paiement
    path('payment-gateways/', PaymentGatewayListView.as_view(), name='payment-gateway-list'),
    path('payment-gateways/<int:pk>/', PaymentGatewayDetailView.as_view(), name='payment-gateway-detail'),
    path('payment-gateways/add/', PaymentGatewayListView.as_view(), name='add-payment-gateway'),  # Utiliser la même vue, ajouter une route

    # Gestion des aéroports
    path('airports/', AirportListView.as_view(), name='airport-list'),
    path('airports/<int:pk>/', AirportDetailView.as_view(), name='airport-detail'),
    path('airports/add/', AddAirportView.as_view(), name='add-airport'),
    path('airports/update/<int:pk>/', UpdateAirportView.as_view(), name='update-airport'),
    path('airports/delete/<int:pk>/', DeleteAirportView.as_view(), name='delete-airport'),

    # Gestion des avions
    path('planes/', PlaneListView.as_view(), name='plane-list'),
    path('planes/<int:pk>/', PlaneDetailView.as_view(), name='plane-detail'),
    path('planes/add/', AddPlaneView.as_view(), name='add-plane'),
    path('planes/update/<int:pk>/', UpdatePlaneView.as_view(), name='update-plane'),
    path('planes/delete/<int:pk>/', DeletePlaneView.as_view(), name='delete-plane'),

    # Gestion des pistes
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('tracks/add/', TrackCreateView.as_view(), name='add-track'),
    path('tracks/update/<int:pk>/', TrackUpdateView.as_view(), name='update-track'),
    path("tracks/delete/<int:pk>/", TrackDeleteView.as_view(), name="delete-track"),
    
    path('tracks/<int:pk>/', TrackCreateView.as_view(), name='track-detail'),

    # Toutes les réservations
    path('all-bookings/', AllBookingsListView.as_view(), name='all-bookings-list'),
]
