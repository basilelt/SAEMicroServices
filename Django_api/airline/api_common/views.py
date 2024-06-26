#api_common/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsStaffUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
import asyncio
import nats
from .to_nats import *
import os
import time
import random

class ObtainAuthToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            user_id_bank = user.id
            token, created = Token.objects.get_or_create(user=user)
            asyncio.run(post_message("banque.creation",f"{user_id_bank}:{random.randint(200:800)}",server="nats://nats:4222"))
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    
     

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for handling individual user details.

    This view allows for retrieving, updating, or deleting user details. Access is restricted to admin users only.

    :model: User
    :serializer: UserSerializer
    :permission_classes: IsAdminUser
    """
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

    def create(self, request):
        data = request.data
        flight = Flight.objects.get(id=data['flight'])
        booking_type_id = data.get('booking_type')  # Expecting an ID for booking_type
        booking_type = get_object_or_404(BookingType, id=booking_type_id)

        booking = Booking.objects.create(
            client=request.user,
            booking_type=booking_type,
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
    permission_classes = [IsAuthenticated]

class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

class PlaneListView(generics.ListCreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAuthenticated]

class PlaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAuthenticated]

class AllBookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

#new-2
class AddFlightView(generics.CreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffUser]

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

    async def vol_cretion(self):
        global nc
        env = os.getenv('DJANGO_ENVIRONMENT', 'development')
        user = os.getenv('NATS_USER', '')
        password = os.getenv('NATS_PASSWORD', '')
        if env == 'development':
            nc = await nats.connect("nats://localhost:4222")
        else:
            nc = await nats.connect("nats://nats:4222",user=user,password=password) 
        try:
            flight_creation = f"{Flight.objects.get(id=self.kwargs.get('pk'))} : {Flight.objects.get(Plane.second_class_capacity.get(id='flight')) + Flight.objects.get(Plane.first_class_capacity.get(id='flight'))}"  
            await nc.publish(f"vol.creation",flight_creation)
        except Exception as e:
            print(e)
        
class UpdateFlightView(generics.UpdateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffUser]

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
    permission_classes = [IsStaffUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# new-2
    def vol_delete():
        env = os.getenv('DJANGO_ENVIRONMENT', 'development')
        user = os.getenv('NATS_USER', '')
        password = os.getenv('NATS_PASSWORD', '')
        server="nats://localhost:4222"
        post_message("vol.delete",f"{Flight.objects.get(id=self.kwargs.get('pk'))}",server)


#class ConfirmBookingView(APIView):
#    permission_classes = [IsAdminUser]
#
#    def post(self, request, *args, **kwargs):
#        booking_id = request.data.get('booking_id')
#        try:
#            booking = Booking.objects.get(id=booking_id)
#            if booking.status == 'pending':
#                booking.status = 'confirmed'
#                booking.save()
#                return Response({'status': 'Booking confirmed'}, status=status.HTTP_200_OK)
#            else:
#                return Response({'error': 'Booking is not in a pending state'}, status=status.HTTP_400_BAD_REQUEST)
#        except Booking.DoesNotExist:
#            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

class AddAirportView(generics.CreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffUser]

class UpdateAirportView(generics.UpdateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffUser]

class DeleteAirportView(generics.DestroyAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffUser]

class AddPlaneView(generics.CreateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsStaffUser]

class UpdatePlaneView(generics.UpdateAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsStaffUser]

class DeletePlaneView(generics.DestroyAPIView):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsStaffUser]

# new-2
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(client=user)

# new-2
class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for handling individual transactions.

    This view allows for retrieving, updating, or deleting a transaction. Access is restricted to authenticated users who are the client of the transaction.

    :model: Transaction
    :serializer: TransactionSerializer
    :permission_classes: IsAuthenticated
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        user = self.request.user
        return Transaction.objects.filter(client=user, pk=self.kwargs.get('pk'))

# new-2
class CancellationRequestListView(generics.ListCreateAPIView):
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CancellationRequest.objects.filter(client=user)

# new-2
class CancellationRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for handling individual cancellation requests.

    This view allows for retrieving, updating, or deleting a cancellation request. Access is restricted to authenticated users who are the client of the request.

    :model: CancellationRequest
    :serializer: CancellationRequestSerializer
    :permission_classes: IsAuthenticated
    """
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CancellationRequest.objects.none()
        user = self.request.user
        return CancellationRequest.objects.filter(client=user, pk=self.kwargs.get('pk'))

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        client_id = booking.client.id
        client = get_object_or_404(User, id=client_id)
        price_seat = booking.booking_type.price
        server ="nats://nats:4222"
        subject="banque.validation"
        message = f"{client_id}:{price_seat}"
        # Simulate payment process. In a real scenario, you would integrate with a payment gateway.
        retour_nats=asyncio.run(request_message(subject,message,server))
        time.sleep(3)

        payment_successful = retour_nats # Replace with True for testing

        

        if payment_successful == 'True':
            booking.status = 'confirmed'
            booking.save()
            
            # Create a new Transaction instance
            transaction = Transaction(
                client=client,
                amount=(booking.booking_type.price),
                status='completed',
                booking=booking
            )
            transaction.save()

            return Response({'status': 'Payment successful and booking confirmed'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)


class TrackCreateView(generics.CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsStaffUser]
    
class TrackListView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    
class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    
class TrackUpdateView(generics.UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsStaffUser]
    
class TrackDeleteView(generics.DestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsStaffUser]