


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from scheduling.models import Availability, Slot
from appointments.models import Appointment

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


