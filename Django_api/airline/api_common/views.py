#api_common/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
import asyncio
import nats

class ObtainAuthToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserListView(generics.ListCreateAPIView):
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
        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to view this page.")
        return Booking.objects.filter(client=user)

    def create(self, request):
        data = request.data
        flight = Flight.objects.get(id=data['flight'])
        booking_type = data.get('booking_type')
        booking = Booking.objects.create(
            client=request.user,
            booking_type=booking_type,
            flight=flight,
        )
        booking.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to view this page.")
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

# 以下是新增视图的权限更新
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

class ConfirmBookingView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        try:
            booking = Booking.objects.get(id=booking_id)
            if booking.status == 'pending':
                booking.status = 'confirmed'
                booking.save()
                return Response({'status': 'Booking confirmed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Booking is not in a pending state'}, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

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

# 根据需要继续添加或更新其他视图的权限设置

# new-2
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(client=user)

# new-2
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        user = self.request.user
        return Transaction.objects.filter(client=user, pk=self.kwargs.get('pk'))

# new-2
class CancellationRequestListView(generics.ListCreateAPIView):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CancellationRequest.objects.filter(client=user)

# new-2
class CancellationRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CancellationRequest.objects.none()
        user = self.request.user
        return CancellationRequest.objects.filter(client=user, pk=self.kwargs.get('pk'))

# new-2
class PaymentGatewayListView(generics.ListCreateAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PaymentGateway.objects.filter(transaction__client=user)

# new-2
class PaymentGatewayDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PaymentGateway.objects.none()
        user = self.request.user
        return PaymentGateway.objects.filter(transaction__client=user, pk=self.kwargs.get('pk'))

    async def valid_payment(self):
        global nc
        nc = await nats.connect("nats://192.168.164.130:4222")
        try:
            client = self.request.user
            flight_reserv = self.request.Flight.objects.get(id=self.kwargs.get('pk'))
            seat = self.request.Flight.objects.get(Plane.objects.get(id=flight_reserv.plane_id).second_class_capacity)+self.request.Flight.objects.get(Plane.objects.get(id=flight_reserv.plane_id).first_class_capacity)
            response = await nc.request(f"banque.validation.{client}",timeout=10)
            response_data = response.data.decode()
            data = response_data.split(",")
            payment=data[0]
            if payment == "True":
                response = await nc.request(f"validation.reservation.place.client",f"{flight_reserv} : {seat}",timeout=10)
                data = response_data.split(",")
                payment=data[0]
        except Exception as e:  
            print(e)

class TrackCreateView(generics.CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    
class TrackListView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    
class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    
class TrackUpdateView(generics.UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    
class TrackDeleteView(generics.DestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
