from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Consultation)
admin.site.register(RequestedTest)
admin.site.register(PrescriptoinItem)