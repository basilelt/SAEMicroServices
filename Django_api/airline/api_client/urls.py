# api_client/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserListView, UpdateUserView, DeleteUserView, FlightListView, BookingCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('flights/', FlightListView.as_view(), name='flight_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='create_booking'),
]
