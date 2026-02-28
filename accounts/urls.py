from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('patient-register/', views.patient_register, name='patient_register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.profile, name='profile'),
    path('admin-register/', views.admin_register, name='admin_register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('users/', views.list_users, name='users_list'),
    path('users/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('', include('django.contrib.auth.urls')),
]