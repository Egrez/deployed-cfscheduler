from django.db import models

from inviter.models import Schedule

# Create your models here.
class Invitee(models.Model):
    invitee_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=250, null=True, blank=True)