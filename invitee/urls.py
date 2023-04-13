from django.urls import path

from . import views

urlpatterns = [
    path('invitee/', views.invitee, name='invitee'),
]