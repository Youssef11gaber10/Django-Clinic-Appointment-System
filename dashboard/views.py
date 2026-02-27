from django.shortcuts import render
# from appointments.models import Appointment

## Fake data
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

patientprofiles = [
    {
        "id": 1,
        "date_of_birth": "1990-05-10",
        "address": "123 Main St",
        "gender": "female",
        "user_id": 2,
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



def get_userapp(user_id):
    """Return the userapp dict matching the given id."""
    return next((u for u in userapps if u["id"] == user_id), None)


def get_doctorprofile(doctor_id):
    """Return the doctor profile matching the given id, with user info merged in."""
    profile = next((d for d in doctorprofiles if d["id"] == doctor_id), None)
    if profile:
        user = get_userapp(profile["user_id"])
        # Merge user fields into the profile so the template has everything in one dict
        return {**profile, "user": user}
    return None


def get_patientprofile(patient_id):
    """Return the patient profile matching the given user_id, with user info merged in."""
    profile = next((p for p in patientprofiles if p["user_id"] == patient_id), None)
    if profile:
        user = get_userapp(profile["user_id"])
        return {**profile, "user": user}
    return None


# ── Views ─────────────────────────────────────────────────────────────────────
from django.shortcuts import render
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


# ── Helpers (dummy data only — remove once models are active) ─────────────────

def get_userapp(user_id):
    return next((u for u in userapps if u["id"] == user_id), None)


def get_doctorprofile(doctor_id):
    profile = next((d for d in doctorprofiles if d["id"] == doctor_id), None)
    if profile:
        user = get_userapp(profile["user_id"])
        return {**profile, "user": user}
    return None


# ── Views ─────────────────────────────────────────────────────────────────────

def patient_dashboard_overview(request):

    allowed_status = {"requested", "confirmed"}

    # ── Next Appointment ──────────────────────────────────────────────────────

    # -- DUMMY --
    request.user.id = 2
    next_appointment_raw = next(
        (
            a for a in appointments
            if a["status"] in allowed_status
            and a["patient_id"] == request.user.id
        ),
        None,
    )
    if next_appointment_raw:
        next_appointment = {
            **next_appointment_raw,
            "doctor": get_doctorprofile(next_appointment_raw["doctor_id"]),
        }
    else:
        next_appointment = None

    # next_appointment = (
    #     Appointment.objects
    #     .filter(patient=request.user.id, status__in=allowed_status)
    #     .select_related("doctor__doctorprofile")
    #     .order_by("created_at")
    #     .first()
    # )

    # ── Context ───────────────────────────────────────────────────────────────

    context = {
        "next_appointment": next_appointment,
    }
    return render(request, "dashboard/patient_dashboard.html", context)