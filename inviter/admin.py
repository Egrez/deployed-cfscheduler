from django.contrib import admin

from .models import Inviter, Schedule

# Register your models here.
admin.site.register(Inviter)
admin.site.register(Schedule)