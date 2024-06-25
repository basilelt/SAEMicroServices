# Django_Frontend/monprojet/monapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import *

class ClientForm(forms.ModelForm):
    """
    A form for creating and updating Client instances.

    This form is linked to the Client model and includes all fields from the model.
    """
    class Meta:
        model = Client
        fields = '__all__'

class StaffForm(forms.ModelForm):
    """
    A form for creating and updating Staff instances.

    This form is linked to the Staff model and includes all fields from the model.
    """
    class Meta:
        model = Staff
        fields = '__all__'

class StaffTypeForm(forms.ModelForm):
    """
    A form for creating and updating StaffType instances.

    This form is linked to the StaffType model and includes all fields from the model.
    """
    class Meta:
        model = StaffType
        fields = '__all__'
        
class RegistrationForm(forms.ModelForm):
    """
    A form for user registration.

    This form extends the ModelForm for the User model, adding a password field with a widget to hide the input.
    """
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
    """
    A form for user login.

    This form includes fields for username and password, with the password field using a widget to hide the input.
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class BookingForm(forms.ModelForm):
    """
    A form for creating and updating Booking instances.

    This form is linked to the Booking model. The fields included are determined by the model's configuration.
    """
    class Meta:
        model = Booking
        fields = ['booking_type', 'client', 'flight']
        
class PaymentForm(forms.Form):
    """
    A form for processing payments.

    This form includes a hidden field for the booking ID and can be extended with additional fields required by the payment method.
    """
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
    # Add other fields as required by your payment method
    
class CancellationRequestForm(forms.ModelForm):
    """
    A form for submitting cancellation requests.

    This form is linked to the CancellationRequest model and includes a hidden booking field and a field for the cancellation reason.
    """
    class Meta:
        model = CancellationRequest
        fields = ['booking', 'reason']
        widgets = {'booking': forms.HiddenInput()}  # Hide this field if set automatically

class CancellationReviewForm(forms.Form):
    """
    A form for reviewing cancellation requests.

    This form can be customized to include fields relevant to the review process of cancellation requests.
    """
    status = forms.ChoiceField(choices=[('approved', 'Approve'), ('rejected', 'Reject')])
    
    
class StaffCreationForm(forms.ModelForm):
    """
    A form for creating Staff instances with additional custom fields or validation.

    This form is linked to the Staff model and can include custom fields or validation logic beyond the model's default configuration.
    """

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
    
class FlightForm(forms.ModelForm):
    """
    A form for creating and updating Flight instances.

    This form is linked to the Flight model and includes all fields from the model.
    """
    class Meta:
        model = Flight
        fields = ['flight_number', 'departure', 'arrival', 'plane', 'track_origin', 'track_destination']
        widgets = {
            'departure': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'arrival': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(FlightForm, self).__init__(*args, **kwargs)
        self.fields['departure'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['arrival'].input_formats = ('%Y-%m-%dT%H:%M',)