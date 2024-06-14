#api_common/views.py

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingSerializer, FlightSerializer
from api_staff.models import Flight

class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        flight = serializer.validated_data['flight']
        if flight.booking_set.count() >= flight.plane.second_class_capacity:
            raise serializers.ValidationError("No available seats for this flight")
        serializer.save(client=self.request.user)

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

class BookingDetailView(generics.RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class SeatCheckView(views.APIView):
    def get(self, request, flight_id, format=None):
        flight = get_object_or_404(Flight, pk=flight_id)
        remaining_seats = flight.plane.second_class_capacity - flight.booking_set.count()
        return Response({'remaining_seats': remaining_seats}, status=status.HTTP_200_OK)

class BookingValidationView(views.APIView):
    def post(self, request, booking_id, format=None):
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.is_valid = True
        booking.save()
        return Response({'status': 'Booking validated'}, status=status.HTTP_200_OK)

class PaymentValidationView(views.APIView):
    def post(self, request, format=None):
        # 假设有逻辑来验证支付
        payment_valid = True
        if payment_valid:
            return Response({'status': 'Payment validated'}, status=status.HTTP_200_OK)
        return Response({'status': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
