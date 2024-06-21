# Django_Frontend/monprojet/monapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Client, Staff, StaffType

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