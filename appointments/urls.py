from django.urls import path
from appointments.views import book_appointment , cancel_appointment , check_in_appointment , complete_appointment , confirm_appointment,mark_no_show_appointment , slot_list,reschedule_page

# app_name = "appointments"

urlpatterns = [
    path("slots/",slot_list, name="slot_list"),
    # Patient
    path("book/<int:slot_id>/", book_appointment, name="book_appointment"),
    path("cancel/<int:appointment_id>/",cancel_appointment, name="cancel_appointment"),
    # Receptionist 
    path("confirm/<int:appointment_id>/", confirm_appointment, name="confirm_appointment"),
    path("check_in/<int:appointment_id>/", check_in_appointment, name="check_in_appointment"),
    path("no_show/<int:appointment_id>/", mark_no_show_appointment, name="mark_no_show"),
    # Doctor 
    path("complete/<int:appointment_id>/", complete_appointment, name="complete_appointment"),
    path("reschedule/<int:appointment_id>/", reschedule_page, name="reschedule_appointment"),
]