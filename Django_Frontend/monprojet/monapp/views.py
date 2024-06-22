import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.http import HttpRequest, HttpResponse

# Create your views here.

def get_api_url(request: HttpRequest) -> str:
    host = request.get_host()
    protocol = 'https://'# if request.is_secure() else 'http://'
    api_url = f'{protocol}api.{host}/api/common/'
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'monapp/login.html', {'form': form})

def view_flights(request):
    api_url = get_api_url(request) + 'flights/'  # Adjusted to include the API endpoint
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an HTTPError if the response was an error
        flights = response.json()
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., endpoint not found, server error)
        return HttpResponse(f"HTTP Error occurred: {http_err}", status=500)
    except requests.exceptions.JSONDecodeError as json_err:
        # Handle JSON decode errors
        return HttpResponse(f"Error decoding JSON: {json_err}", status=500)
    except Exception as err:
        # Handle other possible exceptions
        return HttpResponse(f"An error occurred: {err}", status=500)
    
    return render(request, 'monapp/view_flights.html', {'flights': flights})