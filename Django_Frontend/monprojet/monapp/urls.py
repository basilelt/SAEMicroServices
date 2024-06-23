from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('register/', views.register, name='Register'),
    path('login/', views.login, name='Login'),
    path('flights/', views.view_flights, name='Flights'),
    path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('success/', views.success, name='Success'),
]