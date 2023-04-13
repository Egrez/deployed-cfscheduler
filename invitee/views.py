from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def invitee(request):
    return render(request, "temp-invitee.html")
