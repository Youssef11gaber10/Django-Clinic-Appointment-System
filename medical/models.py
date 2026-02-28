from django.db import models
from django.conf import settings
from appointments.models import Appointment
# j
# # Create your models here.

# if you wana get the patient from consultation 
# consultation.appointment.patient
class Consultation(models.Model):
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment = models.OneToOneField(Appointment,
                                       on_delete=models.CASCADE,
                                       related_name='consultations')
    # created_by = models.ForeignKey(
    # settings.AUTH_USER_MODEL,
    # on_delete=models.SET_NULL,
    # null=True,
    # related_name='consultations_created'
    # )
    
    def __str__(self):
        return f"Consultation #{self.id}"

class PrescriptoinItem (models.Model):
    consultation = models.ForeignKey(Consultation,
    on_delete=models.CASCADE,
    related_name='prescriptions'
    )
    drug_name = models.CharField(max_length=255)
    dose = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.drug_name} - {self.dose} for Consultation {self.consultation.id}"
    

class RequestedTest(models.Model):
    consultation = models.ForeignKey(
    Consultation,
    on_delete=models.CASCADE,
    related_name='tests'
    )
    test_name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    # Test result fields — filled by patient
    # result = models.TextField(blank=True)
    # result_file = models.FileField(upload_to='test_results/', blank=True, null=True)
    # result_updated_at = models.DateTimeField(null=True, blank=True)
    # result_updated_by = models.ForeignKey(
    # settings.AUTH_USER_MODEL,
    # on_delete=models.SET_NULL,
    # null=True, blank=True,
    # related_name='test_results_updated'
    # )
    
    




