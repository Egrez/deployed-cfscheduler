from django import forms
from django.utils.translation import gettext_lazy as _

class ScheduleForm(forms.Form):
	schedulecount = forms.IntegerField(widget=forms.HiddenInput())

	meeting_details = forms.CharField(max_length=255, widget=forms.Textarea(
		attrs={
			"class" : "meeting_details"
		}
	))


	def clean_schedulecount(self):
		schedulecount = self.cleaned_data.get('schedulecount')
		
		if (not(schedulecount)): 
			raise forms.ValidationError(_("Please provide an available time."))

		return schedulecount

	# https://jacobian.org/2010/feb/28/dynamic-form-generation/
	# https://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form
	def __init__(self, *args, **kwargs):
		schedulecount = kwargs.pop('schedulecount', 0)
		super().__init__(*args, **kwargs)
		
		if schedulecount:
			for i in range(int(schedulecount)):
				self.fields['schedule_%s' % i] = forms.DateTimeField(input_formats=['%B %d %Y %H:%M:%S'])

	def get_schedules(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('schedule_'):
				yield (value)