

# slots heavy logic

from datetime import date, datetime, timedelta
from .models import Availability, Slot, DoctorException

# get the days available between the start date and end date of the doctor
def get_days_between(start_date, end_date):
    if isinstance(start_date, datetime):
        start_date = start_date.date()
    else:
        start_date = start_date

    if isinstance(end_date, datetime):  
            end_date = end_date.date()
    else:
        end_date=end_date

    days = []
    current_date = start_date
    while current_date <= end_date:
        days.append(current_date)
        current_date += timedelta(days=1)
    return days


#  get doctor unavailable days from doctor exceptions
def doctor_unavailable_days(doctor, date):
    return DoctorException.objects.filter(doctor=doctor, date=date, is_available=False).exists()


# generate slots for a doctor based on his availability and exceptions
def generate_slots_for_doctor(doctor, date):
    if doctor_unavailable_days(doctor,date):
        return []
    
    # doctor is available on this day - check availability table
    day_of_week = date.strftime('%A').upper()
    availabilities = Availability.objects.filter(doctor=doctor, date_of_week= day_of_week)

    slots_created=0
    for availability in availabilities:
        start_time = datetime.combine(date, availability.start_time)
        end_time = datetime.combine(date, availability.end_time)
        slot_duration = availability.slot_duration
        buffer_time = availability.buffer_time

        while start_time + timedelta(minutes=slot_duration) <= end_time:
            slot_time = start_time + timedelta(minutes=slot_duration)

            Slot.objects.get_or_create(
                doctor=doctor,
                start_time= start_time,
                end_time = slot_time,
                is_available = True
            )

            slots_created += 1
            start_time = slot_time + timedelta(minutes= buffer_time)

    return slots_created

# generate slots in date range
def slot_generator(doctor, start_date, end_date):
    days = get_days_between(start_date, end_date)
    total_slots = 0
    for day in days:
        total_slots += generate_slots_for_doctor(doctor, day)            
    return total_slots

        