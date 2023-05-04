from django.utils.crypto import get_random_string

from django import forms

from django.utils.translation import gettext_lazy as _

class CreateEventForm(forms.Form):
    event_name = forms.CharField(
        label='Event name:',
        validators=[],
        widget = forms.TextInput(attrs = {
            'style' : 'width: 500px; height: 80px; text-align: center; border-radius: 40px; box-shadow: 4px 6px 5px 0 rgba(0, 0, 0, 0.3); margin-top: 150px; margin-left: 200px; font-family: Poppins_bold; font-size: 40px;',
            'placeholder' : 'Event Name',
        }),
    )

    def clean_event_name(self):
        event_name = self.cleaned_data.get('event_name')
        
        if (event_name == 'New Event Name'): 
            raise forms.ValidationError(_("Please indicate an event name"))

        return event_name

class CalendarForm(forms.Form):  
	event_name = forms.CharField(
		label='Event name:',
		validators=[],
		widget = forms.TextInput(attrs = {
			"class" : "text",
            'style' : 'width: 500px; height: 80px; text-align: center; border-radius: 40px; box-shadow: 4px 6px 5px 0 rgba(0, 0, 0, 0.3); margin-top: 150px; margin-left: 200px; font-family: Poppins_bold; font-size: 40px;',
            'placeholder' : 'Event Name',
			"name" : "fname",
		}),
	)

	start_time = forms.TimeField(
		label = "Start time:",
		widget = forms.TimeInput(attrs = {
			'type' : 'time',
            "class" : "dropdown",
            "style" : "left: 853px; margin-bottom: 80px; font-family: Poppins; font-size: 30px; font-weight: bold; color: #f2f2f2;",
		}),
	)

	end_time = forms.TimeField(
		label = "End time:",
		widget = forms.TimeInput(attrs = {
			'type' : 'time',
            "class" : "dropdown",
            "style" : "left: 1465px; margin-bottom: 80px; font-family: Poppins; font-size: 30px; font-weight: bold; color: #f2f2f2;",
		}),
	)

	duration = forms.IntegerField(
        label = "Duration",
        widget = forms.TextInput(attrs= {
        "placeholder" : "Event Duration",
        "type" : "integer",
        "class" : "textEvent",
        "style" : "margin-top: 2%; font-weight: bolder;",
        })
    )

	datecount = forms.IntegerField(widget=forms.HiddenInput())

	# https://jacobian.org/2010/feb/28/dynamic-form-generation/
	# https://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form
	def __init__(self, *args, **kwargs):
		datecount = kwargs.pop('datecount', 0)
		super(CalendarForm, self).__init__(*args, **kwargs)
		
		if datecount:
			for i in range(int(datecount)):
				self.fields['date_%s' % i] = forms.DateField(input_formats=['%d-%m-%Y'])

	def get_dates(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('date_'):
				yield (value)