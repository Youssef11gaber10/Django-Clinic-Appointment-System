from django.forms import ValidationError
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from scheduling.models import Availability, Slot, DoctorException
from .form import GenerateSlotsForm, AvailabilityForm, DoctorExceptionForm
from scheduling.models import Availability
from .form import GenerateSlotsForm, AvailabilityForm
from .services import slot_generator
from django.contrib.auth import get_user_model
from datetime import datetime

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
    
        slots_count = slot_generator(doctor, start_date, end_date)
        messages.success(request,f"Generated {slots_count} successfully")
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

def slot_delete(request, pk):
    obj = get_object_or_404(Slot, pk=pk)
    if request.method == 'POST':
        obj.delete()
        print(f"Deleted slot {obj} with id {pk}")
        messages.success(request, 'Slot removed.')
        return redirect('scheduling:slot_list')
    return render(request, 'scheduling/slot_list.html', {'object': obj})

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
    has_solts = Slot.objects.filter(
            doctor=obj.doctor,  
            start_time__time__gte= obj.start_time,
            start_time__time__lte= obj.end_time,
        ).exists()

    if has_solts:
        messages.error(request, "You can't delete this availability because there are slots generated based on it. Please delete the related slots first.")
        return redirect('scheduling:availability_list')
    
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Availability removed.')
        return redirect('scheduling:availability_list')
    return render(request, 'scheduling/availability_list.html', {'object': obj})

# exception views
@receptionist_required
def exception_list(request):
    exceptions = DoctorException.objects.all().select_related('doctor')
    return render(request, 'scheduling/exception_list.html',{
        'exceptions': exceptions,
    })

@receptionist_required
def exception_add(request):
    if request.method == "POST":
        form = DoctorExceptionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            exception_date = obj.date
            if isinstance(exception_date, datetime):
                exception_date = exception_date.date()

            Slot.objects.filter(
                doctor=obj.doctor,
                start_time__date=exception_date
            # ).update(is_available=False)
            ).update(is_available=False, is_exception=True)

            messages.success(request, "Exception added successfully")
            return redirect('scheduling:exception_list')
    else:
        form = DoctorExceptionForm()

    return render(request, 'scheduling/exception_form.html',{
        'form':form,
        'title' : 'Add Exception'
    })

@receptionist_required
def exception_delete(request, pk):
    obj = get_object_or_404(DoctorException, pk=pk)
    if request.method == "POST":
        obj.delete()
        Slot.objects.filter(
            doctor=obj.doctor,
            start_time__date=obj.date
        ).update(is_available=True, is_exception=False)

        messages.success(request, "Exception removed")
        return redirect("scheduling:exception_list")
    return render(request, 'scheduling/availability_list.html', {'object': obj})