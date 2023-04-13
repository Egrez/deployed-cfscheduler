from django.urls import path

from . import views

urlpatterns = [
    path('inviter/', views.inviter, name='inviter'),
]