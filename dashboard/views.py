from django.shortcuts import render

# Create your views here.
def patient_dashboard(request):
    return render(request, 'dashboard/patient_dashboard.html', {})