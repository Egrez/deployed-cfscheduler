from django.utils.crypto import get_random_string

from django import forms

from django.utils.translation import gettext_lazy as _

class CreateEventForm(forms.Form):
    event_name = forms.CharField(
        label='Event name:',
        validators=[],
        widget = forms.TextInput(attrs = {
            'class' : 'form-control w-100',
        }),
    )

    def clean_event_name(self):
        event_name = self.cleaned_data.get('event_name')
        
        if (event_name == 'New Event Name'): 
            raise forms.ValidationError(_("Please indicate an event name"))

        return event_name