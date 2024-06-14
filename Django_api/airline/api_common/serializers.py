#api_common/serializers.py
from rest_framework import serializers
from .models import Booking, BookingType
from api_staff.models import Flight, Plane, Track
from api_client.models import Client

class BookingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingType
        fields = ['id', 'type']
        ref_name = 'BookingTypeCommon'

class BookingSerializer(serializers.ModelSerializer):
    booking_type = BookingTypeSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'booking_date', 'price', 'booking_type', 'client', 'flight']
        ref_name = 'BookingCommon'

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure', 'arrival', 'plane', 'track_origin', 'track_destination']
        ref_name = 'FlightCommon'

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ['id', 'model', 'first_class_capacity', 'second_class_capacity']
        ref_name = 'PlaneCommon'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'track_number', 'length', 'airport']
        ref_name = 'TrackCommon'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'ClientCommon'
