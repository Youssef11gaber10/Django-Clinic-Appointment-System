from django.urls import path
from . import views
from dashboard.views import recep_home_dashboard,recep_views
app_name = "dashboard"

urlpatterns = [
    path('patient/',  views.patient_dashboard, name='patient_dashboard'),
    path('doctor/',  views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist/',  views.recep_home_dashboard, name='recep_dashboard'),
    path('receptionist/add-availability/', recep_views.add_availability, name='add_availability'),
    path('receptionist/generate-slots/', recep_views.generate_slots_page, name='generate_slots'),
    path('analytics/',  views.analytics, name='analytics'),
]
