from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('appuser_create/', views.appuser_create_view, name='appuser_create'),
    path('staff_create/', views.staff_create_view, name='staff_create'),
    path('booking_create/', views.booking_create_view, name='booking_create'),
    path('flight_create/', views.flight_create_view, name='flight_create'),
]