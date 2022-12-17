from django.urls import path

from . import views

urlpatterns = [
    path('<str:id>/login/', views.signin, name='login'),
]