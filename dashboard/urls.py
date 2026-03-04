from django.urls import path
from . import views
from dashboard.views import recep_dashboard,recep_views
# app_name = "dashboard"

urlpatterns = [
    path('patient/',  views.patient_dashboard, name='patient_dashboard'),
    path('doctor/',  views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist/',  views.recep_dashboard, name='recep_dashboard'),
    path("queue/",views.todays_queue,name="todays_queue"),
    path('analytics/',  views.analytics, name='analytics'),
    path("analytics/export/csv/", views.export_csv, name="export_csv"),
]
