# api_client/urls.py
from django.urls import path
from .views import RegisterView, LoginView, UserListView, UpdateUserView, DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('update-user/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    
]
