from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from scheduling.models import Availability, Slot
from scheduling.services import slot_generator
from appointments.models import Appointment




User = get_user_model()



@login_required
def recep_home_dashboard(request):

    if request.user.role != "receptionist":
        raise PermissionDenied("Only receptionist can access this page")

    doctors = (User.objects.filter(role="doctor").prefetch_related("availabilities", "slots__appointments"))

    context = {"doctors": doctors }
    return render(request, "dashboard/recep_dashboard.html", context)





@login_required
def add_availability(request):
    if request.user.role != "receptionist":
        raise PermissionDenied()
    doctors = User.objects.filter(role="doctor")
    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        date_of_week = request.POST.get("date_of_week")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        slot_duration = request.POST.get("slot_duration")
        buffer_time = request.POST.get("buffer_time")

        doctor = get_object_or_404(User, id=doctor_id)

        Availability.objects.create( 
            doctor=doctor,
        date_of_week=date_of_week,
        start_time=start_time,
        end_time=end_time,
        slot_duration=slot_duration,
        buffer_time=buffer_time,

         )
        
        messages.success(request, "Availability added successfully.")
        return redirect("dashboard:recep_dashboard")

    return render( request,"dashboard/add_availability.html",{"doctors": doctors})



@login_required
def generate_slots_page(request):
    if request.user.role != "receptionist":
        raise PermissionDenied()

    doctors = User.objects.filter(role="doctor")

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        doctor = get_object_or_404(User, id=doctor_id)
        slots_count = slot_generator(doctor, start_date, end_date)

        messages.success(request, f"{slots_count} slots generated successfully.")
        return redirect("dashboard:recep_home")

    return render(request,"dashboard/generate_slots.html",{"doctors": doctors})