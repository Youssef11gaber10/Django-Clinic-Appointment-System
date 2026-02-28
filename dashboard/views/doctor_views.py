from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from appointments.models import Appointment
# from datetime import date

def get_today_appointments(doctor):
    statuses = ["CONFIRMED", "CHECKED_IN"]
    # today = date.today()

    # return (
    #     Appointment.objects
    #     .filter(
    #         doctor=doctor,
    #         status__in=statuses,
    #         slot__start_datetime__date=today,
    #     )
    #     .order_by("checked_in_at")
    #     .select_related(
    #         "slot",
    #         "patient",
    #         "patient__user",
    #     )
    # )

# @login_required
def doctor_dashboard(request):
    pass
    # doctor = request.user.doctorprofile

    # today_queue = get_today_appointments(doctor)


    # context = {
    #     "today_queue":      today_queue,
    # }
    # return render(request, "dashboard/doctor_dashboard.html", context)