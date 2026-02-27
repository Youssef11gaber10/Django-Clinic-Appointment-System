from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserApp, PatientProfile    
import re
from datetime import date

class BaseUserCreationForm(UserCreationForm):
    class Meta:
        model = UserApp
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'first_name', 'last_name', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserApp.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserApp.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^(\+?20)?01[0125]\d{8}$', phone_number):
            raise forms.ValidationError("Phone number must be a valid Egyptian number (e.g., 01012345678 or +201012345678).")
        if UserApp.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("A user with that phone number already exists.")
        return phone_number
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.match(r'^[a-zA-Z]+$', first_name):
            raise forms.ValidationError("First name can only contain letters.")
        if first_name and len(first_name) < 3:
            raise forms.ValidationError("First name must be at least 3 characters long.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-Z]+$', last_name):
            raise forms.ValidationError("Last name can only contain letters.")
        if last_name and len(last_name) < 3:
            raise forms.ValidationError("Last name must be at least 3 characters long.")
        return last_name


class PatientUserCreationForm(BaseUserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    address = forms.CharField(max_length=255, required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=True)
 
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
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = date.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if date_of_birth > today:
                raise forms.ValidationError("Date of birth cannot be in the future.")
            if age > 100:
                raise forms.ValidationError("Age cannot be more than 100 years.")
        return date_of_birth
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) < 10:
            raise forms.ValidationError("Address must be at least 10 characters long.")
        return address
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserApp
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
        
class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'address', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }