from django.urls import path
from . import views

urlpatterns = [
    path('patient/',  views.patient_dashboard, name='patient_dashboard'),
    path('doctor/',  views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist/',  views.recep_dashboard, name='recep_dashboard'),
    path('analytics/',  views.analytics, name='analytics'),
]
