from django.db import models

from django.urls import reverse

# Create your models here.
class Event(models.Model):    
    id = models.CharField(max_length=14, primary_key=True)

    name = models.CharField(max_length=40)

    def get_event_url(self):
        """Returns the URL to access an event."""
        return reverse('event-url', args=[str(self.id)])