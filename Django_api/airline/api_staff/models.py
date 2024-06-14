# api_staff/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class StaffManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email字段必须填写')
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
    staff_type = models.ForeignKey('StaffType', on_delete=models.CASCADE, db_column='staff_type')

    groups = models.ManyToManyField(
        Group,
        related_name='staff_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='staff_permissions',
        blank=True
    )

    class Meta:
        db_table = 'staff'

class StaffType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'staff_type'

class Plane(models.Model):
    model = models.CharField(max_length=100)
    second_class_capacity = models.IntegerField()
    first_class_capacity = models.IntegerField()

    class Meta:
        db_table = 'plane'

class Airport(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'airport'

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, db_column='plane', default=1)
    track_origin = models.ForeignKey('Track', related_name='track_origins', on_delete=models.CASCADE, db_column='track_origin', default=1)
    track_destination = models.ForeignKey('Track', related_name='track_destinations', on_delete=models.CASCADE, db_column='track_destination', default=1)

    class Meta:
        db_table = 'flight'

class Track(models.Model):
    track_number = models.CharField(max_length=10)
    length = models.IntegerField()
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, db_column='airport')

    class Meta:
        db_table = 'track'
