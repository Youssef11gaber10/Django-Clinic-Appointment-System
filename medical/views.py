from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import ListView,CreateView, UpdateView, DetailView, View
from django.views import View
from django.http import HttpResponse,Http404,HttpResponseForbidden
from django.urls import reverse
# from django.db import transaction


# Create your views here.

from appointments.models import Appointment
from .models import Consultation, PrescriptoinItem , RequestedTest
from .forms import (ConsultationForm, PrescriptionItemForm,RequestedTestForm)

def index(request):
    return render(request, "medical/index.html")

def consultation_create(request, appointment_id):
    if not request.user.is_authenticated:
        return redirect("login")

    appointment = get_object_or_404(Appointment, pk=appointment_id)
    print(appointment)
    print(request.user.role )
    if request.user.role != "doctor":
        return redirect("login")
    # if appointment.slot.doctor.user != request.user:
    #     return HttpResponseForbidden()
    print(appointment.status)
    if appointment.status != Appointment.CHECKED_IN:
        return HttpResponseForbidden()
    # if hasattr(appointment, "consultation"):
    #     return redirect("consultation-detail", pk=appointment.consultation.pk)

    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.appointment = appointment
            consultation.save()
            return redirect("consultation_detail", pk=consultation.pk)
    else:
        form = ConsultationForm()

    return render(request, "medical/create_consultation.html", {"form": form})


def consultation_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    if not request.user.is_authenticated:
        return redirect("login")
    # if consultation.appointment.slot.doctor.user != request.user:
    #     return HttpResponseForbidden()

    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            return redirect("consultation_detail", pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)

    return render(request, "medical/edit_consultation.html", {"form": form,"object": consultation })



def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)

    
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    # if user != consultation.appointment.patient and user != consultation.appointment.slot.doctor.user:
    #     return HttpResponseForbidden()

    return render(request, "medical/view_summary.html", {"object": consultation})




# def consultation_delete(request, pk):
#     consultation = get_object_or_404(Consultation, pk=pk)

#     if not request.user.is_authenticated:
#         return redirect("login")
#     # if consultation.appointment.slot.doctor.user != request.user:
#     #     return HttpResponseForbidden()

#     if request.method == "POST":
#         consultation.delete()
#         return redirect("doctor-dashboard")

#     return render(request, "medical/consultation_confirm_delete.html", {"object": consultation})


#prescription views 

def prescription_create(request, consultation_id):

    if not request.user.is_authenticated:
            return redirect("login")
    consultation = get_object_or_404(Consultation, pk=consultation_id)

    # if consultation.appointment.slot.doctor.user != request.user:
    #     return redirect("login")

    if request.method == "POST":
        form = PrescriptionItemForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.consultation = consultation # this for add id of consultation
            prescription.save()
            return redirect("consultation_detail", pk=consultation.pk)
    else:
        form = PrescriptionItemForm()

    return render(request, "medical/add_prescription.html", {"form": form})


def prescription_edit(request, pk):

    prescription = get_object_or_404(PrescriptoinItem, pk=pk)
    if not request.user.is_authenticated:
    
        return redirect("login")

    # if prescription.consultation.appointment.slot.doctor.user != request.user:
    #     return redirect("login")

    if request.method == "POST":
        form = PrescriptionItemForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            # return redirect("consultation_detail", pk=prescription.consultation.pk)
            return redirect( "consultation_detail", pk=prescription.consultation_id)

    else:

        form = PrescriptionItemForm(instance=prescription)

    return render(request, "medical/edit_prescription.html", {"form": form,"object": prescription })




# def prescription_delete(request, pk):
#     prescription = get_object_or_404(PrescriptoinItem, pk=pk)
#     if not request.user.is_authenticated:
#         return redirect("login")
#     if prescription.consultation.appointment.slot.doctor.user != request.user:
#         return HttpResponseForbidden()
#     if request.method == "POST":
#         consultation_id = prescription.consultation.pk
#         prescription.delete()
#         return redirect("consultation-detail", pk=consultation_id)
#     return render(request, "medical/prescription_confirm_delete.html", {"object": prescription})




def add_test(request, consultation_id):

    if not request.user.is_authenticated:
      return redirect("login")
    
    consultation = get_object_or_404(Consultation, pk=consultation_id)

    # if consultation.appointment.slot.doctor.user != request.user:
        #   return redirect("login")

    if request.method == "POST":
        form = RequestedTestForm(request.POST) 

        if form.is_valid():
            test = form.save(commit=False)
            test.consultation = consultation    
            test.save()

            return redirect("consultation_detail", pk=consultation.pk)
    else:
        form = RequestedTestForm()

    return render(request, "medical/add_test.html", {"form": form})
    


def edit_test(request, pk):

    test = get_object_or_404(RequestedTest, pk=pk)

    if not request.user.is_authenticated:
        return redirect("login")

    # if test.consultation.appointment.slot.doctor.user != request.user:
    #     return redirect("login")

    if request.method == "POST":
        form = RequestedTestForm(request.POST, instance=test)
    
        if form.is_valid():
            form.save()
            return redirect("consultation_detail", pk=test.consultation.pk)
    else:
        form = RequestedTestForm(instance=test)

    return render(request, "medical/test_edit.html", {"form": form,"object":test})



# def test_delete(request, pk):
# 
# test = get_object_or_404(RequestedTest, pk=pk)
# 
# 
# 
# if not request.user.is_authenticated:
# 
    # return redirect("login")
# 
# if test.consultation.appointment.slot.doctor.user != request.user:
# 
    # return HttpResponseForbidden()
# 
# if request.method == "POST":
# 
    # consultation_id = test.consultation.pk
# 
    # test.delete()
# 
    # return redirect("consultation-detail", pk=consultation_id)
# 
# return render(request, "medical/test_confirm_delete.html", {"object": test})
# 
# 
# 
# 
# 
# 
# 
def view_summary(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")

    consultation = get_object_or_404(Consultation, pk=pk)

    if request.user.role == "patient":
        if consultation.appointment.patient != request.user:
            return HttpResponseForbidden()
        return render(request, "medical/view_summary.html", {"object": consultation})

    elif request.user.role == "doctor":
        return render(request, "medical/view_summary.html", {"object": consultation})

    else:
        return HttpResponseForbidden()


















