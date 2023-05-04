from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Inviter, Schedule
from event.models import Event

from .forms import ScheduleForm


import datetime

def inviter(request, event_id):
	success = 0
	if 'user' in request.session:
		inviter = get_object_or_404(Inviter, inviter_id=request.session['user'])
		print(inviter)
		existing_schedules = inviter.schedule_set.all()
		print(existing_schedules)
		meeting_details = inviter.meeting_details
		inviter_name = inviter.name
	else:
		return redirect(reverse('signin', args=[event_id]))

	form = ScheduleForm(initial={
		"meeting_details" : meeting_details,
	})
		
	event = get_object_or_404(Event, event_id=event_id)
	share_link = f"{request.get_host()}/{event.share_id}/invitee/"

	date_ranges = event.daterange_set.all()

	available_dates = ""
	for date_range in date_ranges:
		start_date = date_range.start_date
		end_date = date_range.end_date

		delta = end_date - start_date
		
		for i in range(delta.days + 1):
			date = (start_date + datetime.timedelta(days=i))

			if date >= datetime.date.today():
				available_dates += date.isoformat() + ","

	start_time = event.start_time
	end_time = event.end_time

	start_time_delta =  datetime.timedelta(hours=start_time.hour, minutes=start_time.minute) 
	end_time_delta = datetime.timedelta(hours=end_time.hour, minutes=end_time.minute)

	duration = event.duration

	delta = end_time_delta - start_time_delta

	available_times = ""

	for i in range(0, delta.seconds//60 + 1, duration):
		time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=i)).strftime("%H:%M")
		available_times += time + ","

	available_dates = available_dates[:-1]
	available_times = available_times[:-1]

	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = ScheduleForm(data=request.POST, schedulecount=request.POST.get('schedulecount'))

		if form.is_valid():
			schedules = [schedule for schedule in form.get_schedules()]
			meeting_details = form.cleaned_data["meeting_details"]

			inviter.meeting_details = meeting_details
			inviter.save()

			existing_schedules.delete()

			for schedule in schedules:
				print(schedule)
				schedule = Schedule(inviter=inviter, start_datetime=schedule, end_datetime=schedule + datetime.timedelta(minutes=duration), is_booked=False)
				schedule.save()
			success = 1

	existing_schedules = ",".join([sched.start_datetime.isoformat() for sched in existing_schedules])

	context = {
		'month' : datetime.date.strftime(datetime.date.today(), "%B"),
		'year' : datetime.date.strftime(datetime.date.today(), "%Y"),
		'days' : [(datetime.date.today() + datetime.timedelta(days=i+1)).day for i in range(-1, 34)],
		'available_dates' : available_dates,
		'available_times' : available_times,
		'inviter_name' : inviter_name,
		'existing_schedules' : existing_schedules,
		'form' : form,
		'success' : success,
		'share_link' : share_link,
	}

	return render(request, "inviter.html", context)