from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .form import GenerateSlotsForm
from .services import slot_generator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def generate_slots_view(request):
    if request.method == 'POST':
      form = GenerateSlotsForm(request.POST)
      
      form.fields['doctor'].queryset = User.objects.filter(role='doctor')


      if form.is_valid():
        doctor = form.cleaned_data['doctor']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if end_date < start_date:
           messages.error(request, "End date must be after start date")
        else:
           slots_count = slot_generator(doctor, start_date, end_date)
           messages.success(request,f"Generated ${slots_count} successfully")
           return redirect('scheduling:generate_slots')
    else:
        form = GenerateSlotsForm()
        form.fields['doctor'].queryset = User.objects.filter(role='doctor')

    return render(request, 'scheduling/generate_slots.html', {'form': form})
    