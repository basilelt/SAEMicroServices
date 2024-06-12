from django.db import models

# Create your models here.

class AppUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class StaffType(models.Model):
    type = models.CharField(max_length=100)

class Staff(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    staff_type = models.ForeignKey(StaffType, on_delete=models.CASCADE)

class Plane(models.Model):
    model = models.CharField(max_length=100)
    second_class_capacity = models.IntegerField()
    first_class_capacity = models.IntegerField()

class Airport(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Track(models.Model):
    track_number = models.CharField(max_length=10)
    length = models.IntegerField()
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    track_origin = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='departure_flights')
    track_destination = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='arrival_flights')

class BookingType(models.Model):
    type = models.CharField(max_length=30)

class Booking(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

class Working(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)