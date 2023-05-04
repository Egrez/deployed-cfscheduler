from django import forms

class BookingForm(forms.Form):
	schedule_id = forms.IntegerField(widget=forms.HiddenInput())
	name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
		"class" : "text-invitee",
		"placeholder" : "Name",
	}))
	email = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
		"class" : "text-invitee",
		"placeholder" : "Email",
	}))


	message = forms.CharField(max_length=250, widget=forms.Textarea(attrs={
		"class" : "invitee-message",
		"placeholder" : "Message to Inviter",
	}))
