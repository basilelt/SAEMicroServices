# api_common/models.py
from django.db import models
from api_staff.models import Flight
from api_client.models import Client

class BookingType(models.Model):
    type = models.CharField(max_length=30)

    class Meta:
        db_table = 'booking_type'

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    booking_type = models.ForeignKey(BookingType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'booking'
