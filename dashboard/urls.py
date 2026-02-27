from django.urls import path
from . import views

urlpatterns = [
    path('patient/',  views.patient_dashboard, name='patient_dashboard'),
]
