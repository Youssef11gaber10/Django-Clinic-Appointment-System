from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from datetime import date


from datetime import date, time, datetime

today = date.today()

queue_data = [
    {
        "patient": {
            "first_name": "Sara",
            "last_name": "Mohamed",
            "initials": "SM",
            "age": 34,
            "gender": "F",
            "phone": "+20 100 234 5678",
        },
        "slot": {
            "start_datetime": datetime.combine(today, time(9, 0)),
            "end_datetime":   datetime.combine(today, time(9, 30)),
        },
        "status": "CHECKED_IN",
        "reason": "Chest pain follow-up",
        "checked_in_at": datetime.combine(today, time(9, 2)),
        "queue_position": 1,
        "wait_minutes": 28,
    },
    {
        "patient": {
            "first_name": "Karim",
            "last_name": "Youssef",
            "initials": "KY",
            "age": 51,
            "gender": "M",
            "phone": "+20 111 876 5432",
        },
        "slot": {
            "start_datetime": datetime.combine(today, time(9, 30)),
            "end_datetime":   datetime.combine(today, time(10, 0)),
        },
        "status": "CHECKED_IN",
        "reason": "ECG review",
        "checked_in_at": datetime.combine(today, time(9, 35)),
        "queue_position": 2,
        "wait_minutes": 12,
    },
    {
        "patient": {
            "first_name": "Nour",
            "last_name": "El-Din",
            "initials": "NE",
            "age": 29,
            "gender": "F",
            "phone": "+20 122 345 6789",
        },
        "slot": {
            "start_datetime": datetime.combine(today, time(10, 0)),
            "end_datetime":   datetime.combine(today, time(10, 30)),
        },
        "status": "CONFIRMED",
        "reason": "Blood pressure check",
        "checked_in_at": None,
        "queue_position": 3,
        "wait_minutes": None,
    },
]
def get_today_appointments(doctor):
    statuses = ["CONFIRMED", "CHECKED_IN"]
    today = date.today()

    # return (
    #     Appointment.objects
    #     .filter(
    #         doctor=doctor,
    #         status__in=statuses,
    #         slot__start_datetime__date=today,
    #     )
    #     .order_by("checked_in_at")
    #     .select_related(
    #         "slot",
    #         "patient",
    #         "patient__user",
    #     )
    # )

@login_required
def doctor_dashboard(request):

    # today_queue = get_today_appointments(doctor)


    context = {
        "today_queue": queue_data,
    }
    return render(request, "dashboard/doctor_dashboard.html", context)