# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.core.exceptions import PermissionDenied
# from scheduling.models import Availability, Slot
# from scheduling.services import slot_generator
# from appointments.models import Appointment




# User = get_user_model()



# @login_required
# def recep_home_dashboard(request):

#     if request.user.role != "receptionist":
#         raise PermissionDenied("Only receptionist can access this page")

#     doctors = (User.objects.filter(role="doctor").prefetch_related("availabilities", "slots__appointments"))

#     context = {"doctors": doctors }
#     return render(request, "dashboard/recep_dashboard.html", context)





# @login_required
# def add_availability(request):
#     if request.user.role != "receptionist":
#         raise PermissionDenied()
#     doctors = User.objects.filter(role="doctor")
#     if request.method == "POST":

#         doctor_id = request.POST.get("doctor")
#         date_of_week = request.POST.get("date_of_week")
#         start_time = request.POST.get("start_time")
#         end_time = request.POST.get("end_time")
#         slot_duration = request.POST.get("slot_duration")
#         buffer_time = request.POST.get("buffer_time")

#         doctor = get_object_or_404(User, id=doctor_id)

#         Availability.objects.create( 
#             doctor=doctor,
#         date_of_week=date_of_week,
#         start_time=start_time,
#         end_time=end_time,
#         slot_duration=slot_duration,
#         buffer_time=buffer_time,

#          )
        
#         messages.success(request, "Availability added successfully.")
#         return redirect("dashboard:recep_dashboard")

#     return render( request,"dashboard/add_availability.html",{"doctors": doctors})



# @login_required
# def generate_slots_page(request):
#     if request.user.role != "receptionist":
#         raise PermissionDenied()

#     doctors = User.objects.filter(role="doctor")

#     if request.method == "POST":
#         doctor_id = request.POST.get("doctor")
#         start_date = request.POST.get("start_date")
#         end_date = request.POST.get("end_date")
#         doctor = get_object_or_404(User, id=doctor_id)
#         slots_count = slot_generator(doctor, start_date, end_date)

#         messages.success(request, f"{slots_count} slots generated successfully.")
#         return redirect("dashboard:recep_home")

#     return render(request,"dashboard/generate_slots.html",{"doctors": doctors})

# 
# 
# 




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




# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
# from scheduling.models import Availability, Slot
# from appointments.models import Appointment
# from django.contrib.auth.decorators import login_required

# User = get_user_model()

# @login_required
# def recep_dashboard(request):

#     if request.user.role != "receptionist":
#         return redirect("login")

#     doctors = User.objects.filter(role="doctor").select_related("doctor_profile")

#     selected_doctor_id = request.GET.get("doctor")
#     selected_doctor = None
#     availabilities = []
#     slots = []
#     appointments = []

#     if selected_doctor_id:
#         selected_doctor = get_object_or_404(User, id=selected_doctor_id, role="doctor")

#         availabilities = Availability.objects.filter(
#             doctor=selected_doctor
#         ).order_by("date_of_week", "start_time")

#         slots = Slot.objects.filter(
#             doctor=selected_doctor
#         ).select_related("doctor").prefetch_related("appointments").order_by("start_time")

#         appointments = Appointment.objects.filter(
#             slot__doctor=selected_doctor
#         ).select_related("patient", "slot")

#     context = {
#         "doctors": doctors,
#         "selected_doctor": selected_doctor,
#         "availabilities": availabilities,
#         "slots": slots,
#         "appointments": appointments,
#     }

#     return render(request, "dashboard/recep_dashboard.html", context)
