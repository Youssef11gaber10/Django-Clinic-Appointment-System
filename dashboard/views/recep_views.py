from django.shortcuts import render

def recep_dashboard(request):
    return render(request, "dashboard/recep_dashboard.html")