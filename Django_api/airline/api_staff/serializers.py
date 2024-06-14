# api_staff/serializers.py
from rest_framework import serializers
from .models import Flight, Plane, Track, Airport, Staff
from django.contrib.auth import get_user_model, authenticate
from api_common.models import Booking

User = get_user_model()

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ['id', 'model', 'first_class_capacity', 'second_class_capacity']
        ref_name = 'PlaneStaff'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'track_number', 'length', 'airport']
        ref_name = 'TrackStaff'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'name', 'location']
        ref_name = 'AirportStaff'

class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer(read_only=True)
    track_origin = TrackSerializer(read_only=True)
    track_destination = TrackSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure', 'arrival', 'plane', 'track_origin', 'track_destination']
        extra_kwargs = {
            'departure': {'required': False},
            'arrival': {'required': False}
        }
        ref_name = 'FlightStaff'

class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
