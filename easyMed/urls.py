
from django.urls import path
from . import views

urlpatterns = [
    path('homeunimed', views.homeunimed, name = 'homeunimed'),

]
