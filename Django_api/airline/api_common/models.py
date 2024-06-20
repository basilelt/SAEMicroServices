# api_common/models.py
from django.db import models
from django.contrib.auth.models import User

class StaffType(models.Model):
    type = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'staff_type'

class Group(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'group'

class ClientGroups(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'client_groups'

class StaffGroups(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'staff_groups'

class Permission(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'permission'

class ClientPermissions(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'client_permissions'

class StaffPermissions(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'staff_permissions'

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

class Plane(models.Model):
    model = models.CharField(max_length=100)
    second_class_capacity = models.IntegerField()
    first_class_capacity = models.IntegerField()
    
    class Meta:
        db_table = 'plane'

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    track_origin = models.ForeignKey(Track, related_name='departure_flights', on_delete=models.CASCADE)
    track_destination = models.ForeignKey(Track, related_name='arrival_flights', on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight'

class BookingType(models.Model):
    type = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'booking_type'

class Booking(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'booking'

class Working(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'working'

# 新增模型
class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
    reserved_at = models.DateTimeField(auto_now_add=True)
    number_of_tickets = models.IntegerField()
    # Merge this table with Booking table

class Transaction(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'transaction'
        
class CancellationRequest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    reason = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'cancellation_request'

class PaymentGateway(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    gateway_response = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payment_gateway'

class FlightCrew(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)  # 例如 Pilot, Attendant 等
    assigned_at = models.DateTimeField(auto_now_add=True)
    #Merge this table with Working table
