from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientUserCreationForm, BaseUserCreationForm, PatientProfileUpdateForm, UserUpdateForm, DoctorProfileUpdateForm 
from .models import UserApp as User, PatientProfile, DoctorProfile

def patient_register(request):
    if request.method == 'POST':
        form = PatientUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
    else:
        form = PatientUserCreationForm()
    return render(request, 'registration/patient_register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = BaseUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if user.role == 'patient':
                PatientProfile.objects.create(user=user)
            elif user.role == 'doctor':
                DoctorProfile.objects.create(user=user)
            messages.success(request, f'{user.role.capitalize()} account has been created successfully.')
            return redirect('users_list')
    else:
        form = BaseUserCreationForm()
    return render(request, 'registration/admin_register.html', {'form': form})

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
    user = request.user
    context = {
        'user': user,
    }
    if user.role == 'patient':
        try:
         context['profile'] = user.patient_profile
        except PatientProfile.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
    if user.role == 'doctor':
        try:
            context['profile'] = user.doctor_profile
        except DoctorProfile.DoesNotExist:
            messages.error(request, 'Doctor profile not found.')
    return render(request, 'registration/profile.html', context)

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user.role == 'patient':
            try:
                patient_profile = PatientProfile.objects.get(user=user)
                profile_form = PatientProfileUpdateForm(request.POST, instance=patient_profile)
            except PatientProfile.DoesNotExist:
                messages.error(request, 'Patient profile not found.')
                return redirect('profile')
        elif user.role == 'doctor':
            try:
                doctor_profile = DoctorProfile.objects.get(user=user)
                profile_form = DoctorProfileUpdateForm(request.POST, instance=doctor_profile)
            except DoctorProfile.DoesNotExist:
                messages.error(request, 'Doctor profile not found.')
                return redirect('profile')
        else:
            profile_form = None
        
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        if user.role == 'patient':
            try:
                patient_profile = PatientProfile.objects.get(user=user)
                profile_form = PatientProfileUpdateForm(instance=patient_profile)
            except PatientProfile.DoesNotExist:
                messages.warning(request, 'Patient profile not found.')
                profile_form = None
        elif user.role == 'doctor':
            try:
                doctor_profile = DoctorProfile.objects.get(user=user)
                profile_form = DoctorProfileUpdateForm(instance=doctor_profile)
            except DoctorProfile.DoesNotExist:
                messages.warning(request, 'Doctor profile not found.')
                profile_form = None
        else:
            profile_form = None

    return render(request, 'registration/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def list_users(request):
    users = User.objects.all()
    return render(request, 'registration/users_list.html', {'users': users})

def admin_edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'{user.role.capitalize()} account has been updated successfully.')
            return redirect('users_list')
    else:
        user_form = UserUpdateForm(instance=user)
    return render(request, 'registration/edit_profile.html', {'user_form': user_form, 'user': user})

def admin_delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted successfully.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('users_list')