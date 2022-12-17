from django.shortcuts import render

from .forms import CreateEventForm

from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect

import string

from .models import Event

from django.urls import reverse


def event(request):
    if request.method == 'POST':
        form = CreateEventForm(data=request.POST)

        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            event_id = get_random_string(14, string.ascii_letters + string.digits)

            event = Event(id=event_id, name=event_name)
            event.save()

            print()

            return HttpResponseRedirect(reverse("login", args=[event_id]))           

    else:
        form = CreateEventForm(initial={'event_name': 'New Event Name'})

    context = {
        'form': form,
    }

    
    return render(request, "event.html", context)