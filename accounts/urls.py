from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('patient-register/', views.patient_register, name='patient_register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.profile, name='profile'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('', include('django.contrib.auth.urls')),
]