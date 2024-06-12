#api_staff.models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser, Group, Permission

class StaffManager(BaseUserManager):
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

class Staff(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='staff_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='staff_permission_set',
        blank=True
    )

    staff_type = models.ForeignKey('StaffType', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class StaffType(models.Model):
    type = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.type


class Flight(models.Model):
    flight_number = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        verbose_name = 'flight'
        verbose_name_plural = 'flights'
