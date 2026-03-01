from django import forms
from django.contrib.auth import get_user_model
from .models import Availability

User = get_user_model()

# generate slots form
# doctor - start date - end date
class GenerateSlotsForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(role="doctor"), label="Doctor")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Start Date")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="End Date")


# availability form 
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ('doctor', 'date_of_week', 'start_time', 'end_time', 'slot_duration', 'buffer_time')
        widgets = {
            'start_time' : forms.TimeInput(attrs={'type': 'time'}),
            'end_time' : forms.TimeInput(attrs={'type': 'time'}),
        }
         
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(role='doctor')
