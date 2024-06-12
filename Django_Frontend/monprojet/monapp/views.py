import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ClientForm, StaffForm

# Create your views here.

api_url = 'http://localhost:8020/api/'

def client_create_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_staff=data['is_staff'],
                is_superuser=data['is_superuser']
            )
            user.save()
            messages.success(request, 'Client created successfully')
            return redirect('success')
    else:
        form = ClientForm()
    return render(request, 'client_form.html', {'form': form})

def staff_create_view(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                is_staff=data['is_staff'],
                is_superuser=data['is_superuser']
            )
            user.staffprofile.staff_type = data['staff_type']
            user.staffprofile.save()
            user.save()
            messages.success(request, 'Staff created successfully')
            return redirect('success')
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})