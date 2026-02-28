from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(UserApp)