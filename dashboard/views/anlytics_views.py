from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse

from appointments.models import Appointment, RescheduleHistory
from accounts.models import UserApp
from accounts.permissions import require_role


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
        .values("doctor_id", "doctor__username", "doctor__first_name", "doctor__last_name")
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

def get_rescheduled_appointments():
    return RescheduleHistory.objects.select_related(
        "appointment",
        "changed_by"
    )

def get_context():
    return {
        "appointments_insights": get_overall_appointment_metrics(),
        "doctors_insights": get_doctor_appointment_metrics(),
        "total_doctors_patients": get_total_patients_doctors(),
        "daily_insights": get_daily_insights(),
        "monthly_insights": get_monthly_insights(),
        "rescheduled_appointments": get_rescheduled_appointments(),
        "generated_at": timezone.now(),
    }



# Analytics Dashboard View
@login_required(login_url='login')
@require_role('admin')
def analytics(request):
    return render(request, "dashboard/analytics.html", context=get_context())

@login_required(login_url='login')
@require_role('admin')
def export_csv(request):
    response = HttpResponse(
    content_type="text/csv",
    headers={
        "Content-Disposition": 'inline; filename="clinic-analytics.csv"'
        },
    )   
    all_analytics = get_context()


    writer = csv.writer(response)
    writer.writerow(["Generated At", all_analytics["generated_at"]])
    writer.writerow([""])

    writer.writerow(["Total Patients", all_analytics["total_doctors_patients"]["total_patients"]])
    writer.writerow(["Total Doctors", all_analytics["total_doctors_patients"]["total_doctors"]])

    writer.writerow([""])
    writer.writerow(["Appointments Insights"])
    appts_insights = all_analytics["appointments_insights"]
    for key, value in appts_insights.items():
        writer.writerow([ "  ", key, value])

    writer.writerow([""])
    writer.writerow(["Doctors Insights"])
    doctors_insights = all_analytics["doctors_insights"]
    writer.writerow(["Id", "Username", "First Name", "Last Name", "Total Appointments", "Completed Appointments", "Cancelled Appointments", "No Show Appointments", "Requested Appointments", "Confirmed Appointments", "Checked In Appointments"])
    for doctor in doctors_insights:
        writer.writerow([
            doctor["doctor_id"],
            doctor["doctor__username"],
            doctor["doctor__first_name"],
            doctor["doctor__last_name"],
            doctor["total_appointments"],
            doctor["completed_appointments"],
            doctor["cancelled_appointments"],
            doctor["no_show_appointments"],
            doctor["requested_appointments"],
            doctor["confirmed_appointments"],
            doctor["checked_in_appointments"],
    ])
    writer.writerow([""])
    writer.writerow(["Daily Insights"])
    daily_insights = all_analytics["daily_insights"]
    daily_isnights_header = ["Day", "Total_Appointments", "Completed_Appointments", "Cancelled_Appointments", "No _Show_Appointments", "Requested Appointments", "Confirmed Appointments", "Checked In Appointments"]
    for rowKey, key in  zip(daily_isnights_header, daily_insights[0].keys()):
        writer.writerow([ rowKey , daily_insights[0][key]])

    writer.writerow([""])
    writer.writerow(["Monthly Insights"])
    monthly_insights = all_analytics["monthly_insights"]
    monthly_insights_header = daily_isnights_header
    monthly_insights_header[0] = "Month"
    for rowKey, key in  zip(monthly_insights_header, monthly_insights[0].keys()):
        writer.writerow([ rowKey , key == "month" and monthly_insights[0][key].strftime("%Y %B") or monthly_insights[0][key]])

    writer.writerow([""])
    writer.writerow(["Rescheduled Appointments"])
    rescheduled_appointments = all_analytics["rescheduled_appointments"]
    print(rescheduled_appointments)
    writer.writerow(["Appointment ID", "Old Date-Time", "New Date-Time", "Changed By", "Reason", "Logged At"])
    for reschedule in rescheduled_appointments:
        writer.writerow([
        reschedule.appointment.id,
        reschedule.old_start_datetime.strftime("%Y %B %d %I:%M %p"),
        reschedule.new_start_datetime.strftime("%Y %B %d %I:%M %p"),
        reschedule.changed_by.username,
        reschedule.reason,
        reschedule.timestamp.strftime("%Y %B %d"),
    ])   
    
   
    return response