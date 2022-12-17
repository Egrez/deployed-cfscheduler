from django.shortcuts import render

from .forms import LoginForm
from django.contrib.auth import login, authenticate

from event.models import Event

# Create your views here.
def signin(request, id):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = LoginForm(data=request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

                # redirect to a new URL:
                #return HttpResponseRedirect(reverse('home'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = LoginForm(initial={'username': 'serge'})

    event_name = Event.objects.get(id=id).name
    
    context = {
        'form': form,
        'event_name': event_name,
    }

    return render(request, 'login.html', context)