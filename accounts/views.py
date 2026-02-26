from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login(request):
    return render(request, 'registration/login.html', {})

# Create your views here.
