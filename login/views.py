from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.crypto import get_random_string

from .forms import LoginForm

from event.models import Event

import string

from inviter.models import Inviter

def signin(request, event_id):
	event = get_object_or_404(Event, event_id=event_id)

	if request.method == 'POST':
		form = LoginForm(data=request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			try:
				existing_inviter = event.inviter_set.get(name=name)
			except:
				existing_inviter = None
			
			if existing_inviter and existing_inviter.password == password:
				request.session['user'] = existing_inviter.inviter_id
				return redirect(reverse('inviter', args=[event_id]))
			elif existing_inviter and existing_inviter.password != password:
				messages.error(request, "Wrong password")
			else:
				inviter_id = get_random_string(14, string.ascii_letters + string.digits)
				inviter = Inviter(event=event, inviter_id=inviter_id, name=name, email=email, password=password)
				inviter.save()
				request.session['user'] = inviter.inviter_id
				return redirect(reverse('inviter', args=[event_id]))

	else:
		form = LoginForm(initial={
			'name' : 'serge', 
			'email' : 'sergealecrivera@gmail.com', 
			'password' : 'secret'
		})
		
	context = {
		'form' : form,
        'event_name' : event.name,
	}

	return render(request, "SigninPage.html", context=context)