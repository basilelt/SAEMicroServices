from django.shortcuts import render
from .models import AppUser, Staff, Booking, Flight
from .forms import AppUserForm, StaffForm, BookingForm, FlightForm

# Create your views here.

def home(request):
    return render(request, 'monapp/home.html')

def about(request):
    return render(request, 'monapp/about.html')

def appuser_create_view(request):
    form = AppUserForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "monapp/appuser_create.html", context)

def staff_create_view(request):
    form = StaffForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "monapp/staff_create.html", context)

def booking_create_view(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "monapp/booking_create.html", context)

def flight_create_view(request):
    form = FlightForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "monapp/flight_create.html", context)