from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('flights/', views.view_flights, name='flights'),
    path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('success/', views.success, name='success'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('confirm-booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    #path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]