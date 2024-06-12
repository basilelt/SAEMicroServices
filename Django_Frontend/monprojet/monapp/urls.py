from django.urls import path
from . import views

urlpatterns = [
    path('create-client/', views.client_create_view, name='create-client'),
    path('create-staff/', views.staff_create_view, name='create-staff'),
]