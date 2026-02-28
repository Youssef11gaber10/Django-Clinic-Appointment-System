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

