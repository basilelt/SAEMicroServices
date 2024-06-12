# api_staff/urls.py
from django.urls import path
from .views import AddFlightView, DeleteFlightView, UpdateFlightView, FlightListView, StaffLoginView

urlpatterns = [
    path('add-flight/', AddFlightView.as_view(), name='add_flight'),
    path('delete-flight/<int:flight_id>/', DeleteFlightView.as_view(), name='delete_flight'),
    path('update-flight/<int:flight_id>/', UpdateFlightView.as_view(), name='update_flight'),
    path('flights/', FlightListView.as_view(), name='flight_list'),
    path('login/', StaffLoginView.as_view(), name='staff_login'),
]