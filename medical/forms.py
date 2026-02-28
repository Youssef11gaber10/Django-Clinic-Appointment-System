from django import forms
from .models import Consultation, PrescriptoinItem, RequestedTest

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['diagnosis', 'notes']
       

class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptoinItem
        fields = ['drug_name', 'dose', 'duration', 'instructions']


class RequestedTestForm(forms.ModelForm):
    class Meta:
        model = RequestedTest
        fields = ['test_name', 'notes']
