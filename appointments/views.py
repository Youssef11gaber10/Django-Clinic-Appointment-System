from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError , PermissionDenied
from .models import Appointment
from scheduling.models import Slot

def book_appointment(request, slot_id):
    # print("BOOK VIEW CALLED")
    # print(request.method)
    if request.method == "POST":
        slot = get_object_or_404(Slot, id=slot_id)
        try:
            Appointment.request_appointment(slot, request.user)
            messages.success(request, "Appointment booked successfully.")
        except Exception as e:
            print("ERROR:", e)
            raise e
    return redirect("appointments:slot_list")


def cancel_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.cancel_appointment(request.user)
        messages.success(request, "Appointment cancelled successfully.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("dashboard:patient_dashboard")


def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.confirm_appointment(request.user)
        messages.success(request, "Appointment confirmed.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")


def check_in_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.check_in_appointment(request.user)
        messages.success(request, "Patient checked in.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")


def mark_no_show_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.mark_no_show(request.user)
        messages.success(request, "Appointment marked as no-show.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")

def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.complete_appointment(request.user)
        messages.success(request, "Appointment completed.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")

def slot_list(request):
    slots = Slot.objects.filter(is_available=True)
    return render(request, "appointments/view_Slot.html", {"slots": slots})



def reschedule_page(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.patient != request.user:
        return redirect("dashboard:patient_dashboard")

    available_slots = Slot.objects.filter(
        doctor=appointment.slot.doctor,
        is_available=True,
    )
    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        reason = request.POST.get("reason")
        if not available_slots.filter(id=slot_id).exists():
            messages.error(request, "Invalid or unavailable slot selected.")
            return redirect(request.path)
        new_slot = available_slots.get(id=slot_id)

        try:
            appointment.reschedule(new_slot, request.user, reason)
            messages.success(request, "Appointment rescheduled successfully.")
            return redirect("dashboard:patient_dashboard")
        except Exception as e:
            messages.error(request, str(e))

    return render(request, "appointments/reschedule.html", {
        "appointment": appointment,
        "available_slots": available_slots
    })
