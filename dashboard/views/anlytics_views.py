from django.shortcuts import render

def analytics(request):
    return render(request, "dashboard/analytics.html")