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
from rest_framework.permissions import AllowAny

class ObtainAuthToken(APIView):
    permission_classes = (AllowAny,)

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
    #permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAdminUser]

class FlightListView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #permission_classes = [IsAuthenticated]

class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #permission_classes = [IsAuthenticated]

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(client=user)

    def create(self, request):
        data = request.data
        flight = Flight.objects.get(id=data['flight'])
        # Assuming 'client' is a field in 'Booking' model that refers to the user
        booking = Booking.objects.create(
            client=request.user,
            flight=flight,
            # Add other necessary fields from 'data' as needed
        )
        booking.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        user = self.request.user
        return Booking.objects.filter(client=user, pk=self.kwargs.get('pk'))

    #new-2
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'confirmed':
            instance.status = 'canceled'
            instance.save()
            flight = instance.flight
            if instance.booking_type.type == 'second':
                flight.available_second_class_seats += 1
            elif instance.booking_type.type == 'first':
                flight.available_first_class_seats += 1
            flight.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("Only confirmed bookings can be canceled.")

class AirportListView(generics.ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    #permission_classes = [IsAdminUser]

class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    #permission_classes = [IsAdminUser]

class PlaneListView(generics.ListCreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    #permission_classes = [IsAdminUser]

class PlaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    #permission_classes = [IsAdminUser]

class AllBookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    #permission_classes = [IsAdminUser]

#new-2
class AddFlightView(generics.CreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data
        plane = Plane.objects.get(id=data['plane'])
        track_origin = Track.objects.get(id=data['track_origin'])
        track_destination = Track.objects.get(id=data['track_destination'])
        
        flight = Flight.objects.create(
            flight_number=data['flight_number'],
            departure=data['departure'],
            arrival=data['arrival'],
            plane=plane,
            track_origin=track_origin,
            track_destination=track_destination,
            available_second_class_seats=plane.second_class_capacity,
            available_first_class_seats=plane.first_class_capacity
        )
        flight.save()
        return Response(FlightSerializer(flight).data, status=status.HTTP_201_CREATED)

#new-2
class UpdateFlightView(generics.UpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

#new-2
class DeleteFlightView(generics.DestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    #permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# new-2
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
    #permission_classes = [IsAdminUser]

class UpdateAirportView(generics.UpdateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    #permission_classes = [IsAdminUser]

class DeleteAirportView(generics.DestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    #permission_classes = [IsAdminUser]

class AddPlaneView(generics.CreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    #permission_classes = [IsAdminUser]

class UpdatePlaneView(generics.UpdateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    #permission_classes = [IsAdminUser]

class DeletePlaneView(generics.DestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    #permission_classes = [IsAdminUser]

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
