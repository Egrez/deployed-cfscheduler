from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from event.models import Event
from inviter.models import Schedule
from .models import Invitee

from .forms import BookingForm

import json

import datetime

def invitee(request, share_id):
	if (request.method == "POST"):
		form = BookingForm(data=request.POST)

		if form.is_valid():
			event = get_object_or_404(Event, share_id=share_id)

			inviters = event.inviter_set.all()
			if request.session["counter"] == event.counter:
				event.counter = (event.counter + 1) % len(inviters)

				event.save()

				schedule_id = form.cleaned_data["schedule_id"]
				name = form.cleaned_data["name"]
				invitee_email = form.cleaned_data["email"]
				message = form.cleaned_data["message"]

				schedule = Schedule.objects.get(schedule_id=schedule_id)

				schedule.is_booked = True 
				schedule.save()

				invitee = Invitee(schedule=schedule, name=name, email=invitee_email, message=message)
				invitee.save()

				inviter = schedule.inviter

				send_invites(event.name, invitee, inviter, schedule.start_datetime.isoformat(), schedule.end_datetime.isoformat())

				schedules = []
				
				success = 1

				
			else:
				schedules = []
				
				success = 0

				messages.error(request, "Failed to send Google Calendar invites kindly refresh the page.")

				return redirect(reverse('invitee', args=[share_id]))

		
	else:

		event = get_object_or_404(Event, share_id=share_id)

		request.session["counter"] = event.counter

		inviters = event.inviter_set.all()


		success = 0

		form = BookingForm()		

		inviter = inviters[event.counter]

		schedules = inviter.schedule_set.filter(is_booked=False)

		temp = ""
		for schedule in schedules:
			schedule_object = {}
			schedule_object["start"] = schedule.start_datetime.isoformat()
			schedule_object["end"] = schedule.end_datetime.isoformat()
			schedule_object["id"] = schedule.schedule_id

			temp += "." + json.dumps(schedule_object)

		schedules = temp[1:]
	
	context = {
		'month' : datetime.date.strftime(datetime.date.today(), "%B"),
		'year' : datetime.date.strftime(datetime.date.today(), "%Y"),
		'days' : [(datetime.date.today() + datetime.timedelta(days=i+1)).day for i in range(-1, 34)],
		'schedules' : schedules,
		'form' : form,
		'success' : success
	}

	return render(request, "invitee.html", context)


from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import google.oauth2.credentials

# view used to request from spreadsheet 
def send_invites(event_name, invitee, inviter, start_datetime, end_datetime):
	creds = inviter.email_sender_creds

	creds = {
		'token': creds.token,
		'refresh_token': creds.refresh_token,
		'token_uri': creds.token_uri,
		'client_id': creds.client_id,
		'client_secret': creds.client_secret,
	}

	credentials = google.oauth2.credentials.Credentials(**creds)

	# access Google Sheets API with API key
	service = build('calendar', 'v3', credentials=credentials)

	inviter_email = inviter.email
	invitee_email = invitee.email

	meeting_details = inviter.meeting_details
	message = invitee.message

	event = {
		'summary': event_name,
		'description': f"Meeting details:\n {meeting_details}\n\n Invitee message: \n {message}",
		'start': {
			'dateTime': start_datetime,
			'timeZone': 'Asia/Shanghai',
		},
		'end': {
			'dateTime': end_datetime,
			'timeZone': 'Asia/Shanghai',
		},
		'attendees': [
			{'email': inviter_email},
			{'email': invitee_email},
		],
		'reminders': {
			'useDefault': False,
			'overrides': [
			{'method': 'email', 'minutes': 24 * 60},
			{'method': 'popup', 'minutes': 10},
			],
		},

		"guestsCanSeeOtherGuests" : True,
	}

	event = service.events().insert(calendarId="primary", body=event, sendUpdates="all").execute()

	print('Event created: %s' % (event.get('htmlLink')))