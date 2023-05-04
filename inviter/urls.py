from django.urls import path

from . import views

urlpatterns = [
    path('<str:event_id>/inviter/', views.inviter, name='inviter'),
]