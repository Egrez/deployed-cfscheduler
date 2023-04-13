from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def inviter(request):
    return render(request, "inviter.html")