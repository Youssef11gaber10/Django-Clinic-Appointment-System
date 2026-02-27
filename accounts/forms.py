from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserApp, PatientProfile    
import re
from datetime import date

class BaseUserCreationForm(UserCreationForm):
    class Meta:
        model = UserApp
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'first_name', 'last_name', 'role']


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