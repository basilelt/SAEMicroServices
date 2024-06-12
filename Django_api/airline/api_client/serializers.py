# api_client/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from api_staff.models import Flight, Plane, Track
from api_common.models import Booking  # 确保从api_common.models导入Booking
from api_client.models import Client

User = get_user_model()

# api_client/serializers.py
from rest_framework import serializers
from api_common.models import Booking
from api_staff.models import Flight
from api_client.models import Client

class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = ['id', 'model', 'first_class_capacity', 'second_class_capacity']

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'track_number', 'length', 'airport']

class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer(read_only=True)
    track_origin = TrackSerializer(read_only=True)
    track_destination = TrackSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'departure', 'arrival', 'plane', 'track_origin', 'track_destination']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'booking_date', 'price', 'booking_type', 'client', 'flight']

    def create(self, validated_data):
        # 逻辑：如座位验证可以在这里实现
        return Booking.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
