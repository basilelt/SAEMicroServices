#api_common/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Flight, Booking, Airport, Plane, Reservation, Transaction, CancellationRequest, PaymentGateway, FlightCrew

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CancellationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRequest
        fields = '__all__'

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

class FlightCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightCrew
        fields = '__all__'
