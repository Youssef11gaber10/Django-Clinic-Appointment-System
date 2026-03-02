from django.shortcuts import render
from appointments.models import Appointment
from django.db.models import Count, Q
# def get_total_appointements_all_time(request):
#     total_appointments = Appointment.objects.count()
#     return total_appointments

# def get_completed_appointements_all_time(request):
#     completed_appointments = Appointment.objects.filter(status=Appointment.COMPLETED).count()
#     return completed_appointments

# def get_cancelled_appointements_all_time(request):
#     cancelled_appointments = Appointment.objects.filter(status=Appointment.CANCELLED).count()
#     return cancelled_appointments

# def get_no_show_appointements_all_time(request):
#     no_show_appointments = Appointment.objects.filter(status=Appointment.NO_SHOW).count()
#     return no_show_appointments

def get_overall_appointment_metrics():
    return Appointment.objects.aggregate(
        total_appointments=Count("id"),
        completed_appointments=Count("id", filter=Q(status=Appointment.COMPLETED)),
        cancelled_appointments=Count("id", filter=Q(status=Appointment.CANCELLED)),
        no_show_appointments=Count("id", filter=Q(status=Appointment.NO_SHOW)),
        requested_appointments=Count("id", filter=Q(status=Appointment.REQUESTED)),
        confirmed_appointments=Count("id", filter=Q(status=Appointment.CONFIRMED)),
        checked_in_appointments=Count("id", filter=Q(status=Appointment.CHECKED_IN)),
    )


def get_doctor_appointment_metrics():
    return Appointment.objects.values("doctor_id").annotate(
        total_appointments=Count("id"),
        completed_appointments=Count("id", filter=Q(status=Appointment.COMPLETED)),
        cancelled_appointments=Count("id", filter=Q(status=Appointment.CANCELLED)),
        no_show_appointments=Count("id", filter=Q(status=Appointment.NO_SHOW)),
        requested_appointments=Count("id", filter=Q(status=Appointment.REQUESTED)),
        confirmed_appointments=Count("id", filter=Q(status=Appointment.CONFIRMED)),
        checked_in_appointments=Count("id", filter=Q(status=Appointment.CHECKED_IN)),
    )

def analytics(request):

    appointments_insights = get_overall_appointment_metrics()
    doctors_insights = get_doctor_appointment_metrics()


    context ={
        "appointments_insights": appointments_insights,
        "doctors_insights": doctors_insights

    }

    return render(request, "dashboard/analytics.html", context)