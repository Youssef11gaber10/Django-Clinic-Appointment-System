from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment, Slot   
from accounts.models import DoctorProfile
# ── Dummy Data ────────────────────────────────────────────────────────────────

# userapps = [
#     {
#         "id": 1,
#         "username": "dr_smith",
#         "first_name": "John",
#         "last_name": "Smith",
#         "email": "dr.smith@example.com",
#         "role": "doctor",
#         "is_active": True,
#         "phone_number": "1234567890",
#     },
#     {
#         "id": 2,
#         "username": "patient_anna",
#         "first_name": "Anna",
#         "last_name": "Taylor",
#         "email": "anna.taylor@example.com",
#         "role": "patient",
#         "is_active": True,
#         "phone_number": "3456789012",
#     },
# ]

# doctorprofiles = [
#     {
#         "id": 1,
#         "specialization": "Cardiology",
#         "bio": "Heart specialist with 10 years experience",
#         "session_duration": 30,
#         "user_id": 1,
#     }
# ]

# appointments = [
#     {
#         "id": 1,
#         "status": "requested",
#         "created_at": "2026-02-25 10:00:00",
#         "check_in_at": None,
#         "updated_at": "2026-02-25 10:00:00",
#         "patient_id": 2,
#         "doctor_id": 1,
#     },
#     {
#         "id": 2,
#         "status": "confirmed",
#         "created_at": "2026-02-25 11:00:00",
#         "check_in_at": None,
#         "updated_at": "2026-02-25 11:00:00",
#         "patient_id": 2,
#         "doctor_id": 1,
#     },
#     {
#         "id": 3,
#         "status": "completed",
#         "created_at": "2026-02-24 09:30:00",
#         "check_in_at": "2026-02-24 09:30:00",
#         "updated_at": "2026-02-24 10:00:00",
#         "patient_id": 2,
#         "doctor_id": 1,
#     },
# ]


def get_ppointments(patient_id, statuses):
    return Appointment.objects.filter(
        patient_id=patient_id,
        status__in=statuses
        ).select_related("doctor__doctor_profile", "slot").order_by("created_at")


@login_required(login_url="login")
def patient_dashboard(request):

    upcoming_appointments = get_ppointments(request.user.id, ["requested", "confirmed"])
    previous_appointments = get_ppointments(request.user.id, ["completed"])
    appointments_with_info = []

    for appointment in upcoming_appointments:
        appointments_with_info.append({
            "appointment": appointment,
            "doctor": appointment.doctor.doctor_profile, 
            "slot": appointment.slot,
        })
    
    context = {
        "upcoming_appointments":  appointments_with_info,
        "previous_appointments":  previous_appointments
    }
    return render(request, "dashboard/patient_dashboard.html", context)