from django.contrib import admin

# Register your models here.
from .models import Event, DateRange

admin.site.register(Event)
admin.site.register(DateRange)