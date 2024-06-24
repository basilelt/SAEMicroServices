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
    path('book-flight/1/', views.book_flight, name='book_flight_test'),
]