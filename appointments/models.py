from django.db import models
from django.conf import settings
from django.db import transaction , IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist , PermissionDenied
from django.db.models import Q
from django.utils import timezone
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
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['slot'], name = 'unique_slot')
    #     ] 
    @classmethod
    @transaction.atomic
    def request_appointment(cls , slot , user):
        if user.role != "patient":
            raise ValidationError("Only patients can book appointments.")
        active_statuses = [
        cls.REQUESTED,
        cls.CONFIRMED,
        cls.CHECKED_IN,
    ]
        overlapping_exists = cls.objects.filter(
        patient=user,
        status__in=active_statuses,
        slot__start_time__lt=slot.end_time,
        slot__end_time__gt=slot.start_time,
    ).exists()
        
        if overlapping_exists:
            raise ValidationError("You already have an overlapping appointment.")
        
        already_booked = cls.objects.filter(slot=slot, status__in=active_statuses).exists()
        if already_booked:
            raise ValidationError("This slot is already booked.")
        
        if not slot.is_available:
            raise ValidationError("This slot has already been booked.")
        
        try:
            appointment = cls.objects.create(
            slot=slot,
            patient=user,
            doctor = slot.doctor
            )
            slot.is_available = False
            slot.save()
            return appointment
        except IntegrityError:
              raise ValidationError("This slot has been booked by someone else.")
        
    @transaction.atomic
    def confirm_appointment(self , user):
        if user.role != "receptionist":
            raise PermissionDenied("Only receptionists can confirm the appointment.")
        if self.status != self.REQUESTED:
            raise ValidationError("Only appointments with status REQUESTED can be confirmed.")
        self.status = self.CONFIRMED
        self.save()

    
    @transaction.atomic
    def cancel_appointment(self, user):
        if user.role != "patient":
            raise PermissionDenied("Only patient can cancel the appointment.")
        if self.patient != user:
            raise PermissionDenied("You can only cancel your own appointment.")
        if self.status not in [self.REQUESTED , self.CONFIRMED]:
            raise ValidationError("Appointment cannot be cancelled in its current status.")
        self.status = self.CANCELLED
        self.save()
        self.slot.is_available = True
        self.slot.save()


    @transaction.atomic
    def check_in_appointment(self, user):
        if user.role != "receptionist":
            raise PermissionDenied("Only receptionists can check in the appointment.")
        if self.status != self.CONFIRMED:
            raise ValidationError("Only confirmed appointments can be checked in.")
        self.check_in_at = timezone.now()
        self.status = self.CHECKED_IN
        self.save()

    @transaction.atomic
    def mark_no_show(self , user):
        if user.role not in ["receptionist" , "doctor"]:
            raise PermissionDenied("Only receptionist or doctor can mark the appointment.")
        if self.status != self.CONFIRMED:
            raise ValidationError("Only confirmed appointments can be marked as no show.")
        self.status = self.NO_SHOW
        self.save()


    @transaction.atomic
    def complete_appointment(self , user):
        if user.role != "doctor":
            raise PermissionDenied("Only doctor can complete the appointment.")
        if self.status != self.CHECKED_IN:
            raise ValidationError("only checked-in appointments can be completed.")
        try:
            consultation = self.consultation  
        except ObjectDoesNotExist:
            raise ValidationError("consultation required first")
        self.status = self.COMPLETED
        self.save()

    @transaction.atomic
    def reschedule(self, new_slot, user, reason):

        if self.patient != user:
            raise PermissionDenied("You can only reschedule your own appointment.")

        if self.status not in [self.REQUESTED, self.CONFIRMED]:
            raise ValidationError("This appointment cannot be rescheduled.")

        if not new_slot.is_available:
            raise ValidationError("Selected slot is not available.")

        old_start = self.slot.start_time
        self.slot.is_available = True
        self.slot.save()

        self.slot = new_slot
        self.status = self.REQUESTED  
        self.save()

        new_slot.is_available = False
        new_slot.save()

        RescheduleHistory.objects.create(
            appointment=self,
            old_start_datetime=old_start,
            new_start_datetime=new_slot.start_time,
            changed_by=user,
            reason=reason
        )

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




