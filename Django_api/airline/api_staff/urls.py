# api_staff/urls.py
from django.urls import path
from .views import StaffLoginView, AddFlightView, FlightListView, UpdateFlightView, DeleteFlightView

urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='staff_login'),
    path('add-flight/', AddFlightView.as_view(), name='add_flight'),
    path('delete-flight/', DeleteFlightView.as_view(), name='delete_flight'),
    path('flights/', FlightListView.as_view(), name='flight_list'),
    path('update-flight/<int:flight_id>/', UpdateFlightView.as_view(), name='update_flight'),
]
