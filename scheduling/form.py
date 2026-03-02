from django import forms
from django.contrib.auth import get_user_model
from .models import Availability, DoctorException
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model()

# generate slots form
# doctor - start date - end date
class GenerateSlotsForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(role="doctor"), label="Doctor")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Start Date")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="End Date")

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < timezone.now().date():
            raise ValidationError("You can't generate slots for a date in the past")
        return start_date
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date') 
        end_date = cleaned_data.get('end_date') 

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("end date must be after the start date")
            
            delta = end_date - start_date
            if delta.days > 30:
                raise ValidationError("You can't generate slots for more than 30 days")

        return cleaned_data

# availability form 
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ('doctor', 'date_of_week', 'start_time', 'end_time', 'slot_duration', 'buffer_time')
        widgets = {
            'start_time' : forms.TimeInput(attrs={'type': 'time'}),
            'end_time' : forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        slot_duration = cleaned_data.get('slot_duration')
        buffer_time = cleaned_data.get('buffer_time')

        if start_time > end_time:
            raise ValidationError("end time must be after the start time")
        
        if slot_duration <= 0:
            raise ValidationError("slot duration must be greater than 0")

        if buffer_time <= 0:
            raise ValidationError("buffer time must be greater than 0")
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(role='doctor')

# doctor exception form
class DoctorExceptionForm(forms.ModelForm):
    class Meta:
        model = DoctorException
        fields = ('doctor', 'date', 'reason')
        widgets = {
            'date' : forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')

        if date < timezone.now().date():
            raise ValidationError("You can't set exception in the past")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(role = 'doctor')
