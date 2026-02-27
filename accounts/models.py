from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse , get_object_or_404

class UserApp(AbstractUser):
    role = models.CharField(max_length=20, choices=[('doctor', 'Doctor'), 
                                                    ('patient', 'Patient'), 
                                                    ('admin', 'Admin'), 
                                                    ('receptionist', 'Receptionist')], default='patient')
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
    
class DoctorProfile(models.Model):
    user = models.OneToOneField(UserApp, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    session_duration = models.IntegerField(default=30)  
    def __str__(self):
        return f"{self.user.username} - {self.specialization}"
    
class PatientProfile(models.Model):
    user = models.OneToOneField(UserApp, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    def __str__(self):
        return self.user.username
