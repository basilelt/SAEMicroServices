# Django_Frontend/monprojet/monapp/forms.py
from django import forms

class ClientForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)

class StaffForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    staff_type = forms.IntegerField()