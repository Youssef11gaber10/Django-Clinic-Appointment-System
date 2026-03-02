from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserApp, PatientProfile, DoctorProfile    
import re
from datetime import date

class BaseUserCreationForm(UserCreationForm):
    class Meta:
        model = UserApp
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'first_name', 'last_name', 'role']
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            pattern = r'^(\+20|0)?1[0-2]\d{8}$'
            if not re.match(pattern, phone):
                raise forms.ValidationError(
                    'Please enter a valid Egyptian phone number (e.g., +201001234567 or 01001234567)'
                )
            if UserApp.objects.filter(phone_number=phone).exists():
                raise forms.ValidationError('This phone number is already registered.')
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and UserApp.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name) < 3:
            raise forms.ValidationError('First name must be at least 3 characters long.')
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name) < 3:
            raise forms.ValidationError('Last name must be at least 3 characters long.')
        return last_name


class PatientUserCreationForm(BaseUserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    address = forms.CharField(max_length=255, required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=True)
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            age = (date.today() - date_of_birth).days // 365
            if age < 1:
                raise forms.ValidationError('Patient must be at least 1 year old.')
            if age > 120:
                raise forms.ValidationError('Please enter a valid date of birth.')
        return date_of_birth
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) < 10:
            raise forms.ValidationError('Address must be at least 10 characters long.')
        return address
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'  
        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                address=self.cleaned_data.get('address'),
                gender=self.cleaned_data.get('gender')
            )
        return user
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserApp
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            pattern = r'^(\+20|0)?1[0-2]\d{8}$'
            if not re.match(pattern, phone):
                raise forms.ValidationError(
                    'Please enter a valid Egyptian phone number (e.g., +201001234567 or 01001234567)'
                )
            if UserApp.objects.filter(phone_number=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This phone number is already registered.')
        return phone
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and UserApp.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and len(first_name) < 3:
            raise forms.ValidationError('First name must be at least 3 characters long.')
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and len(last_name) < 3:
            raise forms.ValidationError('Last name must be at least 3 characters long.')
        return last_name

class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'address', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            age = (date.today() - date_of_birth).days // 365
            if age < 1:
                raise forms.ValidationError('Patient must be at least 1 year old.')
            if age > 120:
                raise forms.ValidationError('Please enter a valid date of birth.')
        return date_of_birth
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) < 10:
            raise forms.ValidationError('Address must be at least 10 characters long.')
        return address

class DoctorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'bio', 'session_duration', 'session_price']
    def clean_session_price(self):
        price = self.cleaned_data.get('session_price')
        if price:
            if price < 0:
                raise forms.ValidationError('Session price must be a positive number.')
            if price > 10000:
                raise forms.ValidationError('Session price seems too high. Please verify.')
        return price
    def clean_specialization(self):
        specialization = self.cleaned_data.get('specialization')
        if specialization and len(specialization) < 2:
            raise forms.ValidationError('Specialization must be at least 2 characters long.')
        return specialization
    def clean_session_duration(self):
        duration = self.cleaned_data.get('session_duration')
        if duration:
            if duration < 15:
                raise forms.ValidationError('Session duration must be at least 15 minutes.')
            if duration > 60:
                raise forms.ValidationError('Session duration cannot exceed 60 minutes.')
        return duration
