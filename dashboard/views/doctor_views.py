from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from django.utils import timezone
from django.db.models import Q  

from accounts.permissions import require_role
def get_appointments(doctor_id, statuses, date = None):
    return (
        Appointment.objects
        .select_related("patient__patient_profile", "slot")
        .filter(
            doctor_id=doctor_id,
            slot__start_time__date=date,
            status__in=statuses
        )
        .order_by("slot__start_time")
    )

def get_all_completed_appointments(doctor_id):
    return Appointment.objects.filter(doctor_id=doctor_id, status=Appointment.COMPLETED)


@login_required(login_url='login')
@require_role('doctor')
def doctor_dashboard(request):

    today = timezone.localdate()
    doctor_id = request.user.id

    tab = request.GET.get("tab", "queue")  # queue is default
    search = request.GET.get("search")

    if tab == "completed":
        queryset = get_appointments(
            doctor_id,
            [Appointment.COMPLETED],
            today
        )

    elif tab == "all-completed":
        queryset = get_all_completed_appointments(doctor_id)

    else:  # queue
        queryset = get_appointments(
            doctor_id,
            [Appointment.CHECKED_IN],
            today
        )
    if search:
        queryset = queryset.filter(
            Q(patient__first_name__icontains=search) |
            Q(patient__last_name__icontains=search)
        )


    context = {
        "active_tab": tab,
        "appointments": queryset
    }

    return render(request, "dashboard/doctor_dashboard.html", context)