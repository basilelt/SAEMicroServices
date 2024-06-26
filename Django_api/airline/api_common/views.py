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
    """
    Vue API pour obtenir un jeton d'authentification.
    Permet à un utilisateur de s'authentifier et d'obtenir un jeton d'accès.
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Authentifie un utilisateur et renvoie un jeton d'accès.
        
        Args:
            request (Request): La requête HTTP contenant les données d'authentification.

        Returns:
            Response: La réponse contenant le jeton d'accès ou un message d'erreur.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            user_id_bank = user.id
            token, created = Token.objects.get_or_create(user=user)
            asyncio.run(post_message("banque.creation", f"{user_id_bank}:{random.randint(200, 800)}", server="nats://nats:4222"))
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListCreateAPIView):
    """
    Vue API pour lister et créer des utilisateurs.
    Accessible uniquement aux administrateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer un utilisateur.
    Accessible uniquement aux administrateurs.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class FlightListView(generics.ListCreateAPIView):
    """
    Vue API pour lister et créer des vols.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer un vol.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

class BookingListView(generics.ListCreateAPIView):
    """
    Vue API pour lister et créer des réservations.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Récupère les réservations de l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les réservations de l'utilisateur authentifié.
        """
        user = self.request.user
        return Booking.objects.filter(client=user)

    def create(self, request):
        """
        Crée une nouvelle réservation pour l'utilisateur authentifié.
        
        Args:
            request (Request): La requête HTTP contenant les données de la réservation.

        Returns:
            Response: La réponse contenant les données de la réservation créée.
        """
        data = request.data
        flight = Flight.objects.get(id=data['flight'])
        booking_type_id = data.get('booking_type')
        booking_type = get_object_or_404(BookingType, id=booking_type_id)

        booking = Booking.objects.create(
            client=request.user,
            booking_type=booking_type,
            flight=flight,
        )
        booking.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer une réservation.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Récupère les réservations de l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les réservations de l'utilisateur authentifié.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
        user = self.request.user
        return Booking.objects.filter(client=user, pk=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        """
        Annule une réservation confirmée.
        
        Args:
            request (Request): La requête HTTP.

        Returns:
            Response: La réponse indiquant le statut de l'annulation.
        """
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
    """
    Vue API pour lister et créer des aéroports.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

class AirportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer un aéroport.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

class PlaneListView(generics.ListCreateAPIView):
    """
    Vue API pour lister et créer des avions.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAuthenticated]

class PlaneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer un avion.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsAuthenticated]

class AllBookingsListView(generics.ListAPIView):
    """
    Vue API pour lister toutes les réservations.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

class AddFlightView(generics.CreateAPIView):
    """
    Vue API pour ajouter un nouveau vol (personnel uniquement).
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffUser]

    def create(self, request, *args, **kwargs):
        """
        Crée un nouveau vol.
        
        Args:
            request (Request): La requête HTTP contenant les données du vol.

        Returns:
            Response: La réponse contenant les données du vol créé.
        """
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

    async def vol_cretion(self):
        """
        Crée une entrée de vol dans NATS.
        """
        global nc
        env = os.getenv('DJANGO_ENVIRONMENT', 'development')
        user = os.getenv('NATS_USER', '')
        password = os.getenv('NATS_PASSWORD', '')
        if env == 'development':
            nc = await nats.connect("nats://localhost:4222")
        else:
            nc = await nats.connect("nats://nats:4222", user=user, password=password) 
        try:
            flight_creation = f"{Flight.objects.get(id=self.kwargs.get('pk'))} : {Flight.objects.get(Plane.second_class_capacity.get(id='flight')) + Flight.objects.get(Plane.first_class_capacity.get(id='flight'))}"  
            await nc.publish(f"vol.creation", flight_creation)
        except Exception as e:
            print(e)

class UpdateFlightView(generics.UpdateAPIView):
    """
    Vue API pour mettre à jour un vol (personnel uniquement).
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffUser]

    def update(self, request, *args, **kwargs):
        """
        Met à jour un vol.
        
        Args:
            request (Request): La requête HTTP contenant les données du vol.

        Returns:
            Response: La réponse contenant les données du vol mis à jour.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class DeleteFlightView(generics.DestroyAPIView):
    """
    Vue API pour supprimer un vol (personnel uniquement).
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStaffUser]

    def destroy(self, request, *args, **kwargs):
        """
        Supprime un vol.
        
        Args:
            request (Request): La requête HTTP.

        Returns:
            Response: La réponse indiquant le statut de la suppression.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def vol_delete(self):
        """
        Supprime une entrée de vol dans NATS.
        """
        env = os.getenv('DJANGO_ENVIRONMENT', 'development')
        user = os.getenv('NATS_USER', '')
        password = os.getenv('NATS_PASSWORD', '')
        server = "nats://localhost:4222"
        post_message("vol.delete", f"{Flight.objects.get(id=self.kwargs.get('pk'))}", server)

class AddAirportView(generics.CreateAPIView):
    """
    Vue API pour ajouter un nouvel aéroport (personnel uniquement).
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffUser]

class UpdateAirportView(generics.UpdateAPIView):
    """
    Vue API pour mettre à jour un aéroport (personnel uniquement).
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffUser]

class DeleteAirportView(generics.DestroyAPIView):
    """
    Vue API pour supprimer un aéroport (personnel uniquement).
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsStaffUser]

class AddPlaneView(generics.CreateAPIView):
    """
    Vue API pour ajouter un nouvel avion (personnel uniquement).
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsStaffUser]

class UpdatePlaneView(generics.UpdateAPIView):
    """
    Vue API pour mettre à jour un avion (personnel uniquement).
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsStaffUser]

class DeletePlaneView(generics.DestroyAPIView):
    """
    Vue API pour supprimer un avion (personnel uniquement).
    """
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    permission_classes = [IsStaffUser]

class TransactionListView(generics.ListCreateAPIView):
    """
    Vue API pour lister et créer des transactions.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Récupère les transactions de l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les transactions de l'utilisateur authentifié.
        """
        user = self.request.user
        return Transaction.objects.filter(client=user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer une transaction.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Récupère les transactions de l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les transactions de l'utilisateur authentifié.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        user = self.request.user
        return Transaction.objects.filter(client=user, pk=self.kwargs.get('pk'))

class CancellationRequestListView(generics.ListCreateAPIView):
    """
    Vue API pour lister et créer des demandes d'annulation.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Récupère les demandes d'annulation de l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les demandes d'annulation de l'utilisateur authentifié.
        """
        user = self.request.user
        return CancellationRequest.objects.filter(client=user)

class CancellationRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer une demande d'annulation.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = CancellationRequest.objects.all()
    serializer_class = CancellationRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Récupère les demandes d'annulation de l'utilisateur authentifié.
        
        Returns:
            QuerySet: Les demandes d'annulation de l'utilisateur authentifié.
        """
        if getattr(self, 'swagger_fake_view', False):
            return CancellationRequest.objects.none()
        user = self.request.user
        return CancellationRequest.objects.filter(client=user, pk=self.kwargs.get('pk'))

class PaymentView(APIView):
    """
    Vue API pour traiter les paiements.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Traite un paiement pour une réservation.
        
        Args:
            request (Request): La requête HTTP contenant l'ID de la réservation.

        Returns:
            Response: La réponse indiquant le statut du paiement et de la réservation.
        """
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        client_id = booking.client.id
        client = get_object_or_404(User, id=client_id)
        price_seat = booking.booking_type.price
        server = "nats://nats:4222"
        subject = "banque.validation"
        message = f"{client_id}:{price_seat}"
        retour_nats = asyncio.run(request_message(subject, message, server))
        time.sleep(3)

        payment_successful = retour_nats

        if payment_successful == 'True':
            booking.status = 'confirmed'
            booking.save()

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
    """
    Vue API pour ajouter une nouvelle piste (personnel uniquement).
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsStaffUser]

class TrackListView(generics.ListAPIView):
    """
    Vue API pour lister toutes les pistes.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

class TrackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue API pour récupérer, mettre à jour et supprimer une piste.
    Accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]

class TrackUpdateView(generics.UpdateAPIView):
    """
    Vue API pour mettre à jour une piste (personnel uniquement).
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsStaffUser]

class TrackDeleteView(generics.DestroyAPIView):
    """
    Vue API pour supprimer une piste (personnel uniquement).
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsStaffUser]
