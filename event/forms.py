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