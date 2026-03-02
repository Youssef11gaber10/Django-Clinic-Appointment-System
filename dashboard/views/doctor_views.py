from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from django.utils import timezone


def get_appointments(doctor_id, statuses):
    today = timezone.localdate()  
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
    today_appointments = get_appointments(request.user.id,[Appointment.CHECKED_IN])
    compiled_appointments = get_appointments(request.user.id, [Appointment.COMPLETED])
    context = {
        "today_queue": today_appointments,
        "compiled_appointments": compiled_appointments
    }
    return render(request, "dashboard/doctor_dashboard.html", context)