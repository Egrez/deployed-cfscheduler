from django.urls import path

from . import views

urlpatterns = [
    path('<str:event_id>/login/', views.signin, name='signin'),
]