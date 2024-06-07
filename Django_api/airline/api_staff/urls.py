from django.urls import path
from .views import StaffLoginView, AddFlightView, DeleteFlightView

urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='staff_login'),
    path('add-flight/', AddFlightView.as_view(), name='add_flight'),
    path('delete-flight/', DeleteFlightView.as_view(), name='delete_flight'),
]
