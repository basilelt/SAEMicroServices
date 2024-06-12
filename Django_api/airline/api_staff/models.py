from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser, Group, Permission

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
    staff_type = models.ForeignKey('StaffType', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff'
    
    def __str__(self):
        return self.username

class StaffType(models.Model):
    type = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.type

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE)
    track_origin = models.ForeignKey('Track', related_name='track_origins', on_delete=models.CASCADE)
    track_destination = models.ForeignKey('Track', related_name='track_destinations', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'flight'
        verbose_name_plural = 'flights'

    def __str__(self):
        return self.flight_number

class Plane(models.Model):
    model = models.CharField(max_length=100, null=False)
    second_class_capacity = models.IntegerField(null=False)
    first_class_capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.model

class Track(models.Model):
    track_number = models.CharField(max_length=10, null=False)
    length = models.IntegerField(null=False)
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE)

    def __str__(self):
        return self.track_number

class Airport(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class Working(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.staff} working on {self.flight}"

class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
