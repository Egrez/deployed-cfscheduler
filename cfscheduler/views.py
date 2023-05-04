from django.shortcuts import render, redirect

from django.urls import reverse

from event.models import OauthCredentials

def home(request):
    return render(request, "HomePage.html")

    
scopes = ["https://www.googleapis.com/auth/calendar.events"]

from googleapiclient.discovery import build

import google_auth_oauthlib.flow

from cfscheduler.settings import BASE_URL

# permissions set for the Google App to be accessed currently it is set to view and download only
# more permissions here https://developers.google.com/identity/protocols/oauth2/scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# home view
def generate_token(request):

	# create flow from client credentials downloaded from Google cloud
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('creds.json', scopes=SCOPES)

	# URI where the oauth2's response will be redirected this must match with one of the authorized URIs configured in Google Cloud
	flow.redirect_uri = BASE_URL + 'oauthcallback/'

	# configuring the authorization url which will be used to request from oauth2
	authorization_url, state = flow.authorization_url(include_granted_scopes='true')

	# store the state in the session
	request.session['state'] = state
	
	# redirect to the authorization url which will redirect back to the callback view
	return redirect(authorization_url)

# callback used to extract the credentials. this will have a URL with query parameters set to the necessary arguments to extract the credentials e.g. http://localhost/oauthcallback/?state=K15TtnzoBKKepgg0Z3Ph86nEgGiubM&code=4%2F0AWgavdeDqFt44lGsb24OidcJrpSeLUja1OZkhfHNgNsacb00BrKgyeA-6pY7Uw08lt7s9g&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets
def callback(request):
	# get URL of the callback
	response = request.get_full_path()

	# extract the state stored from the home view
	state = request.session['state']

	# create a new flow note that scopes were not defined because it gets appended to the previous scopes
	flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	 'creds.json', scopes=None, state=state)

	# same redirect uri as before
	flow.redirect_uri =  BASE_URL + 'oauthcallback/'

	# function call to get the credentials
	flow.fetch_token(authorization_response=response)

	# store the fetched credentials
	credentials = flow.credentials

	creds = OauthCredentials(token=credentials.token, refresh_token=credentials.refresh_token, token_uri=credentials.token_uri, client_id=credentials.client_id, client_secret=credentials.client_secret)

	creds.save()

	# go back to the home page
	return redirect(reverse('home'))