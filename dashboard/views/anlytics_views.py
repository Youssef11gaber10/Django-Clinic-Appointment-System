from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from appointments.models import Appointment
from accounts.models import UserApp


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
    return (
        Appointment.objects
        .values("doctor_id", "doctor__username")
        .annotate(
            total_appointments=Count("id"),
            completed_appointments=Count("id", filter=Q(status=Appointment.COMPLETED)),
            cancelled_appointments=Count("id", filter=Q(status=Appointment.CANCELLED)),
            no_show_appointments=Count("id", filter=Q(status=Appointment.NO_SHOW)),
            requested_appointments=Count("id", filter=Q(status=Appointment.REQUESTED)),
            confirmed_appointments=Count("id", filter=Q(status=Appointment.CONFIRMED)),
            checked_in_appointments=Count("id", filter=Q(status=Appointment.CHECKED_IN)),
        )
        .order_by("-total_appointments")
    )

def get_total_patients_doctors():
    return UserApp.objects.aggregate(
        total_patients=Count("id", filter=Q(role="patient")),
        total_doctors=Count("id", filter=Q(role="doctor")),
    )
# Daily Insights
def get_daily_insights():
    today = timezone.localdate()
    return (
        Appointment.objects
        .filter(slot__start_time__date=today)  # only today
        .annotate(day=TruncDate("slot__start_time"))
        .values("day")
        .annotate(
            total_appointments=Count("id"),
            completed_appointments=Count("id", filter=Q(status=Appointment.COMPLETED)),
            cancelled_appointments=Count("id", filter=Q(status=Appointment.CANCELLED)),
            no_show_appointments=Count("id", filter=Q(status=Appointment.NO_SHOW)),
            requested_appointments=Count("id", filter=Q(status=Appointment.REQUESTED)),
            confirmed_appointments=Count("id", filter=Q(status=Appointment.CONFIRMED)),
            checked_in_appointments=Count("id", filter=Q(status=Appointment.CHECKED_IN)),
        )
    )

def get_monthly_insights():
    now = timezone.now()
    current_year = now.year
    current_month = now.month

    return (
        Appointment.objects
        .filter(slot__start_time__year=current_year, slot__start_time__month=current_month) 
        .annotate(month=TruncMonth("slot__start_time"))
        .values("month")
        .annotate(
            total_appointments=Count("id"),
            completed_appointments=Count("id", filter=Q(status=Appointment.COMPLETED)),
            cancelled_appointments=Count("id", filter=Q(status=Appointment.CANCELLED)),
            no_show_appointments=Count("id", filter=Q(status=Appointment.NO_SHOW)),
            requested_appointments=Count("id", filter=Q(status=Appointment.REQUESTED)),
            confirmed_appointments=Count("id", filter=Q(status=Appointment.CONFIRMED)),
            checked_in_appointments=Count("id", filter=Q(status=Appointment.CHECKED_IN)),
        )
    )



# Analytics Dashboard View
def analytics(request):
    context = {
        "appointments_insights": get_overall_appointment_metrics(),
        "doctors_insights": get_doctor_appointment_metrics(),
        "total_doctors_patients": get_total_patients_doctors(),
        "daily_insights": get_daily_insights(),
        "monthly_insights": get_monthly_insights(),
        "generated_at": timezone.now(),
    }

    return render(request, "dashboard/analytics.html", context)