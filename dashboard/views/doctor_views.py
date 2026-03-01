from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from django.utils import timezone


def get_today_appointments(doctor_id):
    today = timezone.localdate()  
    statuses = [Appointment.CONFIRMED, Appointment.CHECKED_IN]
    return (
        Appointment.objects
        .select_related("patient__patient_profile", "slot")
        .filter(
            doctor_id=doctor_id,
            slot__start_time__date=today,
            status__in=statuses
        )
        .order_by("slot__start_time")
    )
@login_required
def doctor_dashboard(request):
    today_appointments = get_today_appointments(request.user.id)
    print(today_appointments[0].check_in_at)
    context = {
        "today_queue": today_appointments,
    }
    return render(request, "dashboard/doctor_dashboard.html", context)