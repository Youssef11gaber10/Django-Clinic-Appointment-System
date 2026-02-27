from django.urls import path
from . import views

urlpatterns = [
    path('patient/',  views.patient_dashboard_overview, name='patient_dashboard'),
]
