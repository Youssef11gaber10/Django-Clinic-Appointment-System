


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from scheduling.models import Availability, Slot
from appointments.models import Appointment
from django.utils import timezone
from accounts.permissions import require_role

User = get_user_model()
@login_required
def recep_dashboard(request):
    if request.user.role != "receptionist":
        messages.error(request, "Unauthorized")
        return redirect("login")

    doctors = User.objects.filter(role="doctor")

    selected_doctor_id = request.GET.get("doctor")
    selected_doctor = None
    availabilities = None
    slots = None

    if selected_doctor_id:
        selected_doctor = User.objects.get(id=selected_doctor_id)

        availabilities = Availability.objects.filter(
            doctor=selected_doctor
        )

        slots = Slot.objects.filter(
            doctor=selected_doctor
        ).select_related("doctor").prefetch_related("appointments")

    context = {
        "doctors": doctors,
        "selected_doctor": selected_doctor,
        "availabilities": availabilities,
        "slots": slots,
    }

    return render(request, "dashboard/recep_dashboard.html", context)





@login_required
@require_role('receptionist')
def todays_queue(request):

    today = timezone.localdate()

    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        action = request.POST.get("action")

        appointment = get_object_or_404(Appointment, id=appointment_id)

        if action == "check_in":
            appointment.check_in_appointment(request.user)

        elif action == "no_show":
            appointment.mark_no_show(request.user)

        return redirect("todays_queue")

    appointments = Appointment.objects.filter(
        slot__start_time__date=today,
        status__in=["confirmed", "checked_in", "no_show"]
    ).select_related("patient", "doctor", "slot").order_by("slot__start_time")

    table_appointments = appointments.exclude(status="checked_in")

    queue_appointments = appointments.filter(
        status="checked_in"
    ).order_by("check_in_at")

    context = {
        "table_appointments": table_appointments,
        "queue_appointments": queue_appointments,
        "today": today,
    }

    return render(request, "dashboard/todays_queue.html", context)
    


