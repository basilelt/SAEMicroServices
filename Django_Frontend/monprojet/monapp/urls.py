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
    path('transactions/', views.transactions_view, name='transactions_view'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('confirm-booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('cancel-booking/<int:booking_id>/', views.submit_cancellation_request, name='cancel_booking'),
    path('staff/cancellation-review/', views.staff_review_cancellation_request, name='staff_cancel_review'),
    path('staff/create_staff_user/', views.create_staff_user, name='create_staff_user'),
    path('create_flight/', views.create_flight, name='create_flight'),
    path('flights/<int:flight_id>/update/', views.update_flight, name='update_flight'),
    path('flights/<int:flight_id>/delete/', views.delete_flight, name='delete_flight'),
]