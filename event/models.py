from django.db import models

from django.urls import reverse

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=14, primary_key=True)
    share_id = models.CharField(max_length=14)  # new
    name = models.CharField(max_length=40)
    duration = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    counter = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['share_id'])
        ]

class DateRange(models.Model):
    date_range_id = models.AutoField(primary_key=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class OauthCredentials(models.Model):
    token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    token_uri = models.CharField(max_length=256)
    client_id = models.CharField(max_length=256)
    client_secret = models.CharField(max_length=256)