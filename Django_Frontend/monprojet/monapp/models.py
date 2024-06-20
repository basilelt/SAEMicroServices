from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'client'

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    staff_type = models.ForeignKey('StaffType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff'

class StaffType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'staff_type'

class Group(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'group'

class ClientGroups(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'client_groups'

class StaffGroups(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_groups'

class Permission(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'permission'

class ClientPermissions(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'client_permissions'

class StaffPermissions(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_permissions'

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE)
    track_origin = models.ForeignKey('Track', related_name='departure_flights', on_delete=models.CASCADE)
    track_destination = models.ForeignKey('Track', related_name='arrival_flights', on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight'

class Plane(models.Model):
    model = models.CharField(max_length=100)
    second_class_capacity = models.IntegerField()
    first_class_capacity = models.IntegerField()

    class Meta:
        db_table = 'plane'

class Booking(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    booking_type = models.ForeignKey('BookingType', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        db_table = 'booking'

class BookingType(models.Model):
    type = models.CharField(max_length=30)

    class Meta:
        db_table = 'booking_type'

class Working(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    class Meta:
        db_table = 'working'

class Airport(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'airport'

class Track(models.Model):
    track_number = models.CharField(max_length=10)
    length = models.IntegerField()
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    class Meta:
        db_table = 'track'