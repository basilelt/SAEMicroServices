import requests
import logging
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.http import HttpRequest, HttpResponse

# Create your views here.



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
            return redirect('Login')
    else:
        form = RegistrationForm()
    return render(request, 'monapp/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('Home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'monapp/login.html', {'form': form})

def get_api_url(request: HttpRequest) -> str:
    api_url = 'http://django-api/api/common/'
    return api_url

def view_flights(request):
    api_url = get_api_url(request)
    flights_url = f'{api_url}flights/'
    airports_url = f'{api_url}airports/'
    planes_url = f'{api_url}planes/'
    tracks_url = f'{api_url}tracks/'
    
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        # Make API calls
        flights_response = requests.get(flights_url).json()
        flight_details = []
        
        for flight in flights_response:
            plane = flight['plane']
            plane_response = requests.get(f"{planes_url}{plane}").json()
            
            first_class_capacity = plane_response['first_class_capacity']
            second_class_capacity = plane_response['second_class_capacity']
                
            # Get track origin details
            track_origin = flight['track_origin']
            track_origin_response = requests.get(f"{tracks_url}{track_origin}").json()
            airport_origin_id = track_origin_response['airport']
            airport_origin_response = requests.get(f"{airports_url}{airport_origin_id}").json()
            origin = airport_origin_response['location']
            
            # Get track destination details
            track_destination = flight['track_destination']
            track_destination_response = requests.get(f"{tracks_url}{track_destination}").json()
            airport_destination_id = track_destination_response['airport']
            airport_destination_response = requests.get(f"{airports_url}{airport_destination_id}").json()
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
                'flight_number': flight['flight_number']
            })
                    
        # Render the flight details
        context = {'flight_details': flight_details}
        return render(request, 'monapp/view_flights.html', context)

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")