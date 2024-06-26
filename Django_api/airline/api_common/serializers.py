#api_common/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Flight, Booking, Airport, Plane, Transaction, CancellationRequest, PaymentGateway, Track

class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle User.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_superuser', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur avec les données validées.
        
        Args:
            validated_data (dict): Les données validées pour créer l'utilisateur.

        Returns:
            User: L'utilisateur créé.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class FlightSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Flight.
    """

    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Booking.
    """

    class Meta:
        model = Booking
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Airport.
    """

    class Meta:
        model = Airport
        fields = '__all__'

class PlaneSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Plane.
    """

    class Meta:
        model = Plane
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Transaction.
    """

    class Meta:
        model = Transaction
        fields = '__all__'

class CancellationRequestSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle CancellationRequest.
    """

    class Meta:
        model = CancellationRequest
        fields = '__all__'

class PaymentGatewaySerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle PaymentGateway.
    """

    class Meta:
        model = PaymentGateway
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Track.
    """

    class Meta:
        model = Track
        fields = '__all__'
