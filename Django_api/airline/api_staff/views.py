#api_staff.views
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import StaffLoginSerializer, FlightSerializer
from .models import Flight
from django.contrib.auth import get_user_model
from .serializers import FlightSerializer
from rest_framework import generics

User = get_user_model()

class FlightListView(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class StaffLoginView(APIView):
    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddFlightView(APIView):
    def post(self, request):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Flight added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteFlightView(APIView):
    def delete(self, request):
        flight_id = request.data.get('flight_id')
        try:
            flight = Flight.objects.get(id=flight_id)
            flight.delete()
            return Response({"message": "Flight deleted successfully"}, status=status.HTTP_200_OK)
        except Flight.DoesNotExist:
            return Response({"message": "Flight not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateFlightView(APIView):
    def patch(self, request, flight_id):
        flight = Flight.objects.get(id=flight_id)
        serializer = FlightSerializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Flight updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)