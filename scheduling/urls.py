
from django.urls import path
from .views import generate_slots_view, slot_delete, slot_list,availability_add, availability_delete, availability_list, exception_add, exception_delete, exception_list
app_name = 'scheduling'

urlpatterns = [
    path('generate-slots/',generate_slots_view,name="generate_slots"),
    path('slot/list/', slot_list, name="slot_list"),
    path('slot/delete/<int:pk>/', slot_delete, name="slot_delete"),
    path('availability/add/', availability_add, name="availability_add"),
    path('availability/delete/<int:pk>/', availability_delete, name="availability_delete"),
    path('availability/list/', availability_list, name="availability_list"),
    path('exception/add/', exception_add, name="exception_add"),
    path('exception/delete/<int:pk>/', exception_delete, name="exception_delete"),
    path('exception/list/', exception_list, name="exception_list"),
]
