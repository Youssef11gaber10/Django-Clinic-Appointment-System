from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError , PermissionDenied
from .models import Appointment
from scheduling.models import Slot
from accounts.models import DoctorProfile
from django.contrib.auth.decorators import login_required
from accounts.permissions import require_role
from django.db import transaction

@login_required(login_url='login')
@require_role('patient')
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
    return redirect("patient_dashboard")

@login_required(login_url='login')
@require_role('patient')
def cancel_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.cancel_appointment(request.user)
        messages.success(request, "Appointment cancelled successfully.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("patient_dashboard")


@login_required(login_url='login')
@require_role('receptionist')
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.confirm_appointment(request.user)
        messages.success(request, "Appointment confirmed.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("recep_dashboard")

@login_required(login_url='login')
@require_role('receptionist')
def check_in_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.check_in_appointment(request.user)
        messages.success(request, "Patient checked in.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")

@login_required(login_url='login')
@require_role('doctor')
def mark_no_show_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.mark_no_show(request.user)
        messages.success(request, "Appointment marked as no-show.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("")

@login_required(login_url='login')
@require_role('doctor')
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    try:
        appointment.complete_appointment(request.user)
        messages.success(request, "Appointment completed.")
    except (ValidationError, PermissionDenied) as e:
        messages.error(request, str(e))
    return redirect("doctor_dashboard")


@login_required(login_url='login')
@require_role('patient')
def slot_list(request):
    slots = Slot.objects.filter(is_available=True)
    return render(request, "appointments/view_Slot.html", {"slots": slots})



# def reschedule_page(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id)

#     if appointment.patient != request.user:
#         return redirect("patient_dashboard")

#     available_slots = Slot.objects.filter(
#         doctor=appointment.slot.doctor,
#         is_available=True,
#     )
#     if request.method == "POST":
#         slot_id = request.POST.get("slot_id")
#         reason = request.POST.get("reason")
#         if not available_slots.filter(id=slot_id).exists():
#             messages.error(request, "Invalid or unavailable slot selected.")
#             return redirect(request.path)
#         new_slot = available_slots.get(id=slot_id)

#         try:
#             appointment.reschedule(new_slot, request.user, reason)
#             messages.success(request, "Appointment rescheduled successfully.")
#             return redirect("patient_dashboard")
#         except Exception as e:
#             messages.error(request, str(e))

#     return render(request, "appointments/reschedule.html", {
#         "appointment": appointment,
#         "available_slots": available_slots
#     })

@login_required(login_url='login')
@require_role('patient')
def doctor_list(request):
    doctors = DoctorProfile.objects.all()
    return render(request , "appointments/doctor_list.html" , {"doctors": doctors})

@login_required(login_url='login')
@require_role('patient')
@transaction.atomic
def doctor_slots(request, doctor_id):
    doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor_user = doctor_profile.user 

    if request.method == "POST":
        slot_id = request.POST.get("slot_id")

        slot = get_object_or_404(
            Slot,
            id=slot_id,
            doctor=doctor_user
        )

        try:
            Appointment.request_appointment(slot, request.user)
            messages.success(request, "Appointment booked successfully.")
            return redirect("patient_dashboard")

        except ValidationError as e:
            messages.error(request, str(e))

    slots = Slot.objects.filter(
        doctor=doctor_user,
        is_available=True
    )

    return render(request, "appointments/doctor_slots.html", {
        "slots": slots,
        "doctor": doctor_profile
    })

@login_required(login_url='login')
@require_role('patient')
@transaction.atomic
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.patient != request.user:
        raise PermissionDenied("You can only reschedule your own appointment.")

    doctor_user = appointment.doctor
    doctor_profile = get_object_or_404(DoctorProfile, user=doctor_user)

    if request.method == "POST":
        slot_id = request.POST.get("slot_id")
        reason = request.POST.get("reason", "Rescheduled by patient")

        if not slot_id:
            messages.error(request, "Please select a slot.")
            return redirect("appointments:reschedule", appointment_id=appointment.id)

        new_slot = get_object_or_404(
            Slot,
            id=slot_id,
            doctor=doctor_user,
            is_available=True
        )

        try:
            appointment.reschedule(
                new_slot=new_slot,
                user=request.user,
                reason=reason
            )
            messages.success(request, "Appointment rescheduled successfully.")
            return redirect("patient_dashboard")

        except (ValidationError, PermissionDenied) as e:
            messages.error(request, str(e))

    available_slots = Slot.objects.filter(
        doctor=doctor_user,
        is_available=True
    ).exclude(id=appointment.slot.id)

    return render(request, "appointments/reschedule.html", {
        "appointment": appointment,
        "doctor": doctor_profile,
        "available_slots": available_slots
    })