from django.db import models
from django.contrib.auth.models import User

class Airport(models.Model):
    """
    Represents an airport, including details like location and capacity.
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        db_table = 'airport'

class Track(models.Model):
    """
    Represents a track within an airport for flights takeoff and landing.
    """
    track_number = models.CharField(max_length=10)
    length = models.IntegerField()
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    class Meta:
        db_table = 'track'

class Group(models.Model):
    """
    Represents a group for organizing users or permissions.
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'group'

class Permission(models.Model):
    """
    Represents a permission that can be assigned to groups or directly to users.
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'permission'

class StaffType(models.Model):
    """
    Defines different types of staff roles within the system.
    """
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'staff_type'

class Plane(models.Model):
    """
    Represents an airplane, including model and capacity details.
    """
    model = models.CharField(max_length=100)
    second_class_capacity = models.IntegerField()
    first_class_capacity = models.IntegerField()

    class Meta:
        db_table = 'plane'

class Flight(models.Model):
    """
    Represents a flight, including details like the plane used, route, and schedule.
    """
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey('Plane', on_delete=models.CASCADE)
    track_origin = models.ForeignKey('Track', related_name='departure_flights', on_delete=models.CASCADE)
    track_destination = models.ForeignKey('Track', related_name='arrival_flights', on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight'

class BookingType(models.Model):
    """
    Defines different types of bookings, such as economy, business, or first class.
    """
    type = models.CharField(max_length=30)
    price = models.FloatField()

    class Meta:
        db_table = 'booking_type'

class Booking(models.Model):
    """
    Represents a booking made by a client, including details like booking type and status.
    """
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending', choices=[('pending', 'pending'), ('confirmed', 'confirmed'), ('cancelled', 'cancelled')])
    
    class Meta:
        db_table = 'booking'

class Client(models.Model):
    """
    Represents a client in the system, linked to the Django User model.
    Includes flags for staff and superuser status, primarily for permission management.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        db_table = 'client'

class Staff(models.Model):
    """
    Represents staff members, linked to the Django User model.
    Includes staff status, superuser status, and a foreign key to StaffType for role management.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    staff_type = models.ForeignKey('StaffType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff'

class ClientGroups(models.Model):
    """
    Associates clients with groups for permission and organization purposes.
    """
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'client_groups'

class StaffGroups(models.Model):
    """
    Associates staff members with groups for permission and organization purposes.
    """
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_groups'

class ClientPermissions(models.Model):
    """
    Associates permissions with clients for access control.
    """
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

    class Meta:
        db_table = 'client_permissions'

class StaffPermissions(models.Model):
    """
    Associates permissions with staff members for access control.
    """
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    permission = models.ForeignKey('Permission', on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_permissions'

class Working(models.Model):
    """
    Represents the working details of staff, such as schedules and locations.
    """
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)

    class Meta:
        db_table = 'working'
        
class CancellationRequest(models.Model):
    """
    Represents a request to cancel a booking, including the reason and status of the request.
    """
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Consider removing if not needed
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # Add this line
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending', choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'cancellation_request'
