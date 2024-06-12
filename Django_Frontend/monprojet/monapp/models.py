from django.db import models

# Create your models here.

class Client(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField('Group', through='ClientGroups')
    permissions = models.ManyToManyField('Permission', through='ClientPermissions')

class Staff(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    staff_type = models.ForeignKey('StaffType', on_delete=models.CASCADE)
    groups = models.ManyToManyField('Group', through='StaffGroups')
    permissions = models.ManyToManyField('Permission', through='StaffPermissions')

class StaffType(models.Model):
    type = models.CharField(max_length=100)

class Group(models.Model):
    name = models.CharField(max_length=100)

class ClientGroups(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

class StaffGroups(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

class Permission(models.Model):
    name = models.CharField(max_length=100)

class ClientPermissions(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

class StaffPermissions(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE)
    track_origin = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='departure_flights')
    track_destination = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='arrival_flights')

class Plane(models.Model):
    model = models.CharField(max_length=100)
    second_class_capacity = models.IntegerField()
    first_class_capacity = models.IntegerField()

class Booking(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    booking_type = models.ForeignKey('BookingType', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)

class BookingType(models.Model):
    type = models.CharField(max_length=30)

class Working(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)

class Airport(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Track(models.Model):
    track_number = models.CharField(max_length=10)
    length = models.IntegerField()
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE)