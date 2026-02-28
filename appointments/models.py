from django.db import models
from django.conf import settings
from scheduling.models import Slot
# Create your models here.
class Appointment(models.Model):
    slot = models.ForeignKey(Slot , on_delete=models.CASCADE , related_name="appointments")
    patient = models.ForeignKey(settings.AUTH_USER_MODEL , 
                                on_delete= models.CASCADE ,
                                related_name="patient_appointments",
                                limit_choices_to={'role': 'patient'})
    
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL , 
                                on_delete= models.CASCADE ,
                                related_name="doctor_appointments",
                                limit_choices_to={'role': 'doctor'})
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

    STATUS_CHOICES = [
        (REQUESTED , "requested"),
        (CONFIRMED , "confirmed"),
        (CHECKED_IN , "checked_in"),
        (COMPLETED , "completed"),
        (CANCELLED , "cancelled"),
        (NO_SHOW , "no_show")
    ]
    status = models.CharField(max_length=30 , choices=STATUS_CHOICES,default=REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    check_in_at = models.DateTimeField(null=True , blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot'], name = 'unique_slot')
        ] 

    def __str__(self):
        return f"Appointment #{self.id} - {self.patient.username}"

class RescheduleHistory(models.Model):
    appointment = models.ForeignKey("Appointment" , 
                                    on_delete=models.CASCADE , 
                                    related_name="reschedules")
    old_start_datetime = models.DateTimeField()
    new_start_datetime = models.DateTimeField()
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL ,
                                    on_delete= models.SET_NULL ,
                                    null=True , 
                                    related_name="rescheduled_by_who")
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reschedule for Appointment {self.appointment.id}"




