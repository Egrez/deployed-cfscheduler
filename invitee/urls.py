from django.urls import path

from . import views

urlpatterns = [
    path('<str:share_id>/invitee/', views.invitee, name='invitee'),
]