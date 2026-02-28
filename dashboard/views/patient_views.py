from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import Appointment, DoctorProfile

# ── Dummy Data ────────────────────────────────────────────────────────────────

userapps = [
    {
        "id": 1,
        "username": "dr_smith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "dr.smith@example.com",
        "role": "doctor",
        "is_active": True,
        "phone_number": "1234567890",
    },
    {
        "id": 2,
        "username": "patient_anna",
        "first_name": "Anna",
        "last_name": "Taylor",
        "email": "anna.taylor@example.com",
        "role": "patient",
        "is_active": True,
        "phone_number": "3456789012",
    },
]

doctorprofiles = [
    {
        "id": 1,
        "specialization": "Cardiology",
        "bio": "Heart specialist with 10 years experience",
        "session_duration": 30,
        "user_id": 1,
    }
]

appointments = [
    {
        "id": 1,
        "status": "requested",
        "created_at": "2026-02-25 10:00:00",
        "check_in_at": None,
        "updated_at": "2026-02-25 10:00:00",
        "patient_id": 2,
        "doctor_id": 1,
    },
    {
        "id": 2,
        "status": "confirmed",
        "created_at": "2026-02-25 11:00:00",
        "check_in_at": None,
        "updated_at": "2026-02-25 11:00:00",
        "patient_id": 2,
        "doctor_id": 1,
    },
    {
        "id": 3,
        "status": "completed",
        "created_at": "2026-02-24 09:30:00",
        "check_in_at": "2026-02-24 09:30:00",
        "updated_at": "2026-02-24 10:00:00",
        "patient_id": 2,
        "doctor_id": 1,
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_userapp(user_id):
    return next((u for u in userapps if u["id"] == user_id), None)


def get_doctorprofile(doctor_id):
    profile = next((d for d in doctorprofiles if d["id"] == doctor_id), None)
    if profile:
        user = get_userapp(profile["user_id"])
        return {**profile, "user": user}
    return None


# ── Views ─────────────────────────────────────────────────────────────────────


@login_required(login_url="login")
def patient_dashboard(request):

    active_statuses   = {"requested", "confirmed"}
    previous_statuses = {"completed"}

    request.user.id = 2
    upcoming_appointments = [
        {**app, "doctor": get_doctorprofile(app["doctor_id"])}
        for app in appointments
        if app["patient_id"] == request.user.id
        and app["status"] in active_statuses
    ]

    previous_appointments = [
        {**app, "doctor": get_doctorprofile(app["doctor_id"])}
        for app in appointments
        if app["patient_id"] == request.user.id
        and app["status"] in previous_statuses
    ]

    # upcoming_appointments = (
    #     Appointment.objects
    #     .filter(patient=request.user, status__in=active_statuses)
    #     .select_related("doctor__doctorprofile")
    #     .order_by("created_at")
    # )
    # previous_appointments = (
    #     Appointment.objects
    #     .filter(patient=request.user, status__in=previous_statuses)
    #     .select_related("doctor__doctorprofile")
    #     .order_by("-created_at")
    # )

    context = {
        "upcoming_appointments":  upcoming_appointments,
        "previous_appointments":  previous_appointments,
    }
    return render(request, "dashboard/patient_dashboard.html", context)