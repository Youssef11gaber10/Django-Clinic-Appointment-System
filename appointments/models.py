from django.db import models
# from accounts.models import UserApp
# from scheduling.models import Slot
# Create your models here.
class Appointment(models.Model):
    # slot = models.ForeignKey(Slot , on_delete=models.CASCADE , related_name="appointments")
    # patient = models.ForeignKey(UserApp , on_delete= models.CASCADE ,related_name="patient_appointment")
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
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['slot'], name = 'unique_slot')
    #     ] 

    # def __str__(self):
    #     return f"Appointment #{self.id} - {self.patient.username}"





