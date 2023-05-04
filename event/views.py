from django.shortcuts import render, redirect

from django.utils.crypto import get_random_string
from .forms import CalendarForm

import string
import datetime

from .models import Event

from django.urls import reverse

from event.models import Event, DateRange


def event(request):
# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = CalendarForm(data=request.POST, datecount=request.POST.get('datecount'))

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			event_name = form.cleaned_data['event_name']

			start_time = form.cleaned_data['start_time'] 
			end_time = form.cleaned_data['end_time'] 

			duration = form.cleaned_data['duration'] 

			event_id = get_random_string(14, string.ascii_letters + string.digits)
			share_id = get_random_string(14, string.ascii_letters + string.digits)

			event = Event(event_id=event_id, share_id=share_id, name=event_name, start_time=start_time, end_time=end_time, duration=duration)

			event.save()

			dates = [date for date in form.get_dates()]

			date_ranges = []
			start_date = dates[0]

			if len(dates) == 1:
				date_ranges.append([start_date, start_date])
			else:
				for index in range(1, len(dates)):
					if (dates[index] - dates[index-1] > datetime.timedelta(days=1)):
						end_date = dates[index-1]
						date_ranges.append((start_date, end_date))
						start_date = dates[index]

				end_date = dates[index]
				date_ranges.append((start_date, end_date))


			for date_range in date_ranges:
				date_range = DateRange(event=event, start_date=date_range[0], end_date=date_range[1])
				date_range.save()

			

			# redirect to a new URL:
			return redirect(reverse('signin', args=[event_id]))

	# If this is a GET (or any other method) create the default form.
	else:
		form = CalendarForm()
	
	
	context = {
		'form' : form,
		'month' : datetime.date.strftime(datetime.date.today(), "%B"),
		'year' : datetime.date.strftime(datetime.date.today(), "%Y"),
		'days' : [(datetime.date.today() + datetime.timedelta(days=i+1)).day for i in range(-1, 34)],
	}
	
	return render(request, "CreateEventPage.html", context)