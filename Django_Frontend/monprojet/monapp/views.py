import requests
import logging
import os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import *
from .models import *
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

logging.basicConfig(level=logging.INFO)

ENVIRONNEMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

def get_api_url():
    if ENVIRONNEMENT != 'development':
        api_url = 'http://django-api/api/common/'
    else:
        api_url = 'http://localhost:8010/api/common/'
    return api_url

def client_create_view(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'monapp/create_client.html', {'form': form})

def staff_create_view(request):
    form = StaffForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'monapp/create_staff.html', {'form': form})

def staff_type_create_view(request):
    form = StaffTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'monapp/create_staff_type.html', {'form': form})

def view_staff(request):
    staff = Staff.objects.all()
    return render(request, 'monapp/view_staff.html', {'staff': staff})

def view_clients(request):
    clients = Client.objects.all()
    return render(request, 'monapp/view_clients.html', {'clients': clients})

def view_staff_types(request):
    staff_types = StaffType.objects.all()
    return render(request, 'monapp/view_staff_types.html', {'staff_types': staff_types})

def success(request):
    return render(request, 'monapp/success.html')

def home(request):
    return render(request, 'monapp/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'monapp/register.html', {'form': form})

def login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return HttpResponseRedirect('home')  # Redirect them to a home page or another appropriate page

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Assuming the API endpoint for getting token is '/api/token/'
                # and it expects 'username' and 'password' as POST data
                response = requests.post(get_api_url() + 'token/', data={'username': username, 'password': password})
                if response.status_code == 200:
                    token = response.json().get('token')
                    # Store the token in session or send as a cookie
                    request.session['auth_token'] = token
                    # Redirect to home with token in session
                    return redirect('home')
                else:
                    messages.error(request, 'Failed to retrieve authentication token.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'monapp/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')  # Redirect to a page of your choice, e.g., the home page

def view_flights(request):
    api_url = get_api_url()
    
    token = request.session.get('auth_token')
    
    headers = {
            'Authorization': f'Token {token}',
        }
    
    
    flights_url = f'{api_url}flights/'
    airports_url = f'{api_url}airports/'
    planes_url = f'{api_url}planes/'
    tracks_url = f'{api_url}tracks/'
    
    
    
    
    try:
        # Make API calls
        flights_response = requests.get(flights_url, headers=headers).json()
        flight_details = []
        
        for flight in flights_response:
            plane = flight['plane']
            plane_response = requests.get(f"{planes_url}{plane}", headers=headers).json()
            
            first_class_capacity = plane_response['first_class_capacity']
            second_class_capacity = plane_response['second_class_capacity']

            # Get track origin details
            track_origin = flight['track_origin']
            track_origin_response = requests.get(f"{tracks_url}{track_origin}", headers=headers).json()
            airport_origin_id = track_origin_response['airport']
            airport_origin_response = requests.get(f"{airports_url}{airport_origin_id}", headers=headers).json()
            origin = airport_origin_response['location']

            # Get track destination details
            track_destination = flight['track_destination']
            track_destination_response = requests.get(f"{tracks_url}{track_destination}", headers=headers).json()
            airport_destination_id = track_destination_response['airport']
            airport_destination_response = requests.get(f"{airports_url}{airport_destination_id}", headers=headers).json()
            destination = airport_destination_response['location']
            
            # Format departure and arrival times
            departure = datetime.strptime(flight['departure'].rstrip('Z'), '%Y-%m-%dT%H:%M:%S').strftime('%m/%d/%Y-%H:%M')
            arrival = datetime.strptime(flight['arrival'].rstrip('Z'), '%Y-%m-%dT%H:%M:%S').strftime('%m/%d/%Y-%H:%M')  
            # Append flight details for rendering
            flight_details.append({
                'first_class_capacity': first_class_capacity,
                'second_class_capacity': second_class_capacity,
                'origin': origin,
                'destination': destination,
                'departure': departure,
                'arrival': arrival,
                'flight_number': flight['flight_number'],
                'id': flight['id'],
            })
                    
        # Render the flight details
        context = {'flight_details': flight_details}
        return render(request, 'monapp/view_flights.html', context)

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return HttpResponse("An error occurred while fetching flight data.", status=500)
    except ValueError as e:
        logging.error(f"Value error: {e}")
        return HttpResponse("An error occurred while processing flight data.", status=500)

def book_flight(request, flight_id):
    if not request.user.is_authenticated:
        return HttpResponse('You must be logged in to book a flight.', status=401)

    api_url = get_api_url() + 'bookings/'

    token = request.session.get('auth_token')

    if request.method == 'POST':
        booking_type = request.POST.get('booking_type')
        booking_type = int(booking_type)


        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json',
        }

        data = {
            'client_id': request.user.id,
            'booking_type': booking_type,
            'flight': flight_id,
        }

        try:
            logging.info(f'Sending POST request to {api_url} with headers {headers} and data {data}')
            response = requests.post(api_url, headers=headers, json=data)

            if response.status_code == 201:
                booking_id = response.json().get('id')  # Example, adjust based on actual response structure
                return redirect('confirm_booking', booking_id=booking_id)
            else:
                return HttpResponse(f'Booking failed. Please try again later. Error: {response.text}')
        except requests.exceptions.RequestException as e:
            logging.error(f'Request error: {e}')
        except Exception as e:
            logging.error(f'Unexpected error: {e}')

    return render(request, 'monapp/book_flight.html', {'flight_id': flight_id})

def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process payment here
            # On successful payment:
            return redirect('confirm_booking', booking_id=booking.id)
    else:
        form = PaymentForm(initial={'booking_id': booking_id})
    return render(request, 'monapp/payment.html', {'form': form, 'booking': booking})

def view_bookings(request):
    if not request.user.is_authenticated:
        return HttpResponse('You must be logged in to view your bookings.', status=401)

    api_url = get_api_url() + 'bookings/'  # Make sure this is the correct endpoint
    token = request.session.get('auth_token')

    headers = {
        'Authorization': f'Token {token}',
    }

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            bookings = response.json()
        else:
            return HttpResponse('Failed to fetch bookings. Please try again later.', status=response.status_code)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f'Request error: {e}', status=500)

    return render(request, 'monapp/user_bookings.html', {'bookings': bookings})


def confirm_booking(request, booking_id):
    if request.method == 'POST':
        # Redirect to the payment page
        return redirect('payment', booking_id=booking_id)
    else:
        booking = get_object_or_404(Booking, id=booking_id)
        flight = booking.flight
        # Add any additional logic here if needed to fetch or format flight details
        context = {'booking': booking, 'flight': flight}
        return render(request, 'monapp/confirm_booking.html', context)
    