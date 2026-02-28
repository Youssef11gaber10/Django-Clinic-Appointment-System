from django import forms
from django.contrib.auth import get_user_model


# generate slots form
# doctor - start date - end date

class GenerateSlotsForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=get_user_model().objects.filter(role="doctor"), label="Doctor")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Start Date")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="End Date")
