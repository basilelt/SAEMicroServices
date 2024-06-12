# Django_Frontend/monprojet/monapp/forms.py
from django import forms
from .models import AppUser, Staff, Booking, Flight

class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'