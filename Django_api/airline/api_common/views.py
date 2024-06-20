#api_common/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import Flight, Booking, Airport, Plane, Transaction, CancellationRequest, PaymentGateway
from .serializers import UserSerializer, FlightSerializer, BookingSerializer, AirportSerializer, PlaneSerializer, TransactionSerializer, CancellationRequestSerializer, PaymentGatewaySerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class FlightListView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(client=user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        user = self.request.user
        return Booking.objects.filter(client=user, pk=self.kwargs.get('pk'))

class AirportListView(generics.ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

class PlaneListView(generics.ListCreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

class PlaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

class AllBookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]

class AddFlightView(generics.CreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminUser]

class UpdateFlightView(generics.UpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminUser]

class DeleteFlightView(generics.DestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminUser]

class AddAirportView(generics.CreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

class UpdateAirportView(generics.UpdateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

class DeleteAirportView(generics.DestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminUser]

class AddPlaneView(generics.CreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

class UpdatePlaneView(generics.UpdateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

class DeletePlaneView(generics.DestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAdminUser]

# new
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(client=user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        user = self.request.user
        return Transaction.objects.filter(client=user, pk=self.kwargs.get('pk'))

class CancellationRequestListView(generics.ListCreateAPIView):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CancellationRequest.objects.filter(client=user)

class CancellationRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CancellationRequest.objects.none()
        user = self.request.user
        return CancellationRequest.objects.filter(client=user, pk=self.kwargs.get('pk'))

class PaymentGatewayListView(generics.ListCreateAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PaymentGateway.objects.filter(transaction__client=user)

class PaymentGatewayDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PaymentGateway.objects.none()
        user = self.request.user
        return PaymentGateway.objects.filter(transaction__client=user, pk=self.kwargs.get('pk'))
