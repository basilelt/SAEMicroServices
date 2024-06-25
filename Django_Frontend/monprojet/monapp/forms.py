# Django_Frontend/monprojet/monapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import *

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class StaffTypeForm(forms.ModelForm):
    class Meta:
        model = StaffType
        fields = '__all__'
        
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            client = Client(user=user)
            client.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_type', 'client', 'flight']
        
class PaymentForm(forms.Form):
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
    # Add other fields as required by your payment method
    
class CancellationRequestForm(forms.ModelForm):
    class Meta:
        model = CancellationRequest
        fields = ['booking', 'reason']
        widgets = {'booking': forms.HiddenInput()}  # Hide this field if set automatically

class CancellationReviewForm(forms.Form):
    status = forms.ChoiceField(choices=[('approved', 'Approve'), ('rejected', 'Reject')])
    
    
class StaffCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    is_staff = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput())  # Make is_staff hidden and non-required
    staff_type = forms.ModelChoiceField(queryset=StaffType.objects.all(), initial=1)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'staff_type')
        
    def save(self, commit=True):
        user = super(StaffCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Ensure is_staff is always True regardless of form input
        if commit:
            user.save()
            staff = Staff(user=user)
            staff.save()
        return user