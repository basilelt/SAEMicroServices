# api_client/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class ClientManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class Client(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='client_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='client_permission_set',
        blank=True
    )

    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.username
