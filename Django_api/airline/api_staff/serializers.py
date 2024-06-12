# api_staff/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Flight
from rest_framework import serializers
from .models import Flight, Plane, Track

User = get_user_model()

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure', 'arrival', 'plane', 'track_origin', 'track_destination']
        extra_kwargs = {
            'departure': {'required': False},
            'arrival': {'required': False}
        }


class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

