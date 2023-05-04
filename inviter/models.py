from django.db import models

from event.models import Event

# Create your models here.
class Inviter(models.Model):
    inviter_id = models.CharField(max_length=14, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50)
    meeting_details = models.CharField(max_length=250, null=True, blank=True)

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    inviter = models.ForeignKey('Inviter', on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_booked = models.BooleanField()