from django.http import HttpRequest
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ClientForm, StaffForm, StaffTypeForm, RegistrationForm
from .models import Staff, Client, StaffType
from django.http import HttpRequest

# Create your views here.

def get_api_url(request: HttpRequest) -> str:
    host = request.get_host()
    protocol = 'https://' if request.is_secure() else 'http://'
    api_url = f'{protocol}api.{host}/'
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
    api_url = get_api_url(request) 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        login_url = f'{api_url}/login/'

        response = requests.post(login_url, data={
            'username': username,
            'password': password,
        })

        if response.status_code == 200:
            # Login successful, redirect to home page
            return redirect('home')
        else:
            # Login failed, show error message
            messages.error(request, 'Login failed. Please check your username and password.')
    
    return render(request, 'monapp/login.html')