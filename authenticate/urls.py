
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name = 'home1'),
    path('login/', views.login_user, name='login'),
    path('home', views.home1, name='home1'),
    path('update/', views.update, name='update'),
]
