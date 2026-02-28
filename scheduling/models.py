from django.db import models
from django.conf import settings
from django.db import transaction

# Create your models here.

# slots
class Slot(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available= models.BooleanField(default=True)

    class Meta:
        # configuration class to prevent a doctor from having 2 slots at the same time  
        constraints = [
            models.UniqueConstraint(fields =[ 'doctor', 'start_time'] , name='unique_doctor_slot')
        ]
        ordering = ['start_time']

    def __str__(self):
        return f"{self.doctor} | {self.start_time.strftime('%Y-%m-%d %H:%M')}"    

class Appointment(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "REQUESTED" , "Requested" 
        CONFIRMED = "CONFIRMED" , "Confirmed" 
        CHECK_IN = "CHECK_IN" , "Check_in"
        COMPLETED = "COMPLETED" , "Completed"
        CANCELLED = "CANCELLED", "Cancelled" 
        NO_SHOW = "NO_SHOW" , "No_show"

    status = models.CharField( max_length=50, choices=Status.choices, default = Status.REQUESTED)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "patient_appointment")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "doctor_appointment")
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE, related_name = "appointment")
    check_in_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # buffer_minutes = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.patient} - {self.slot.start_time}"


class RescheduleHistory(models.Model):
    old_datetime = models.DateTimeField()
    new_datetime = models.DateTimeField()
    changed_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reschedule_history")
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="history")

    def __str__(self):
        return f"Reschedule on {self.timestamp.strftime('%Y-%m-%d %H:%M')} for {self.appointment}"

# ensure no double booking for the same slot
@transaction.atomic
def book_appointment(patient, slot):
    if slot.is_booked:
        raise ValueError("This slot is already booked.")
    
    appointment = Appointment.objects.create(patient=patient, slot=slot)
    slot.is_booked = True
    slot.save()
    return appointment

class Availability(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = "MONDAY", "Monday"
        TUESDAY = "TUESDAY", "Tuesday"
        WEDNESDAY = "WEDNESDAY", "Wednesday"
        THURSDAY = "THURSDAY", "Thursday"
        FRIDAY = "FRIDAY", "Friday"
        SATURDAY = "SATURDAY", "Saturday"
        SUNDAY = "SUNDAY", "Sunday"

    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities')
    date_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_exception = models.BooleanField(default=False)
    slot_duration = models.PositiveIntegerField(default=15)
    buffer_time = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ('doctor', 'date_of_week', 'start_time')

    def __str__(self):
        return f"{self.doctor} - {self.date_of_week} from {self.start_time} to {self.end_time}"


# doctor exception for specific date
class DoctorException(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exceptions')
    date = models.DateField()
    reason = models.TextField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date')

    def __str__(self):
        return f"{self.doctor} - {self.date} : {self.reason}"

