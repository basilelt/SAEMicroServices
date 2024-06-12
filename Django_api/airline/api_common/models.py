# api_common/models.py
from django.db import models
from api_staff.models import Flight
from api_client.models import Client

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, db_column='flight')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_column='client')
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'booking'
