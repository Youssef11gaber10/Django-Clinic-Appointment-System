from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import UserApp as User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
        else:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('/accounts/profile/')  
            else:
                messages.error(request, f'Invalid credentials for user: {username}')
    
    return render(request, 'registration/login.html', context)

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def forgot_password(request):
    context = {}
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            new_password = request.POST.get('new_password', '')
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now log in with your new password.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, f'No account found for username: {username}')
    return render(request, 'registration/forgot_password.html', context)

@login_required(login_url='login')
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})


# Create your views here.
