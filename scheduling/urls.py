
from django.urls import path
from .views import generate_slots_view
app_name = 'scheduling'

urlpatterns = [
    path('generate-slots/',generate_slots_view,name="generate_slots")
]
