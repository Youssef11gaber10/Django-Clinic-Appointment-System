from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse , get_object_or_404

class UserApp(AbstractUser):
    role = models.CharField(max_length=20, choices=[('doctor', 'Doctor'), 
                                                    ('patient', 'Patient'), 
                                                    ('admin', 'Admin'), 
                                                    ('receptionist', 'Receptionist')], default='patient')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
