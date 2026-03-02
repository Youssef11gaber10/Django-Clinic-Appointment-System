from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from scheduling.models import Availability, Slot
from .form import GenerateSlotsForm, AvailabilityForm
from .services import slot_generator
from django.contrib.auth import get_user_model

User = get_user_model()

def receptionist_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        if getattr(request.user, 'role', None) != 'receptionist':
            messages.error(request, 'Only receptionists can manage availability.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

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
    
def slot_list(request):
    slots = Slot.objects.all().select_related('doctor')
    return render(request, 'scheduling/slot_list.html', {
        'slots': slots,
    })

#  availability views
@receptionist_required
def availability_list(request):
    availabilities = Availability.objects.all().select_related('doctor')
    return render(request, 'scheduling/availability_list.html', {
        'availabilities': availabilities,
    })
    
@receptionist_required
def availability_add(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'Availability added.')
            return redirect('scheduling:availability_list')
    else:
        form = AvailabilityForm()
    
    return render(request, 'scheduling/availability_form.html', {
        'form': form,
        'title': 'Add availability'
    })


def availability_delete(request, pk):
    obj = get_object_or_404(Availability, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Availability removed.')
        return redirect('scheduling:availability_list')
    return render(request, 'scheduling/availability_list.html', {'object': obj})