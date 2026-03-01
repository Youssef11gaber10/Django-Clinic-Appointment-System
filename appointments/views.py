from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError , PermissionDenied
from .models import Appointment, Slot


def book_appointment(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)
    try:
        Appointment.request_appointment(slot, request.user)
        messages.success(request, "Appointment booked successfully.")
    except ValidationError as e:
        messages.error(request, e.message)
    return redirect("")  


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.cancel_appointment(request.user)
        messages.success(request, "Appointment cancelled successfully.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")


def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.confirm_appointment(request.user)
        messages.success(request, "Appointment confirmed.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("dashboard:recep_dashboard")


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