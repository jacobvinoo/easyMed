from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from easyMed.models import Practice, Doctor, Patient, Appointment
from django.template import Context, Template
from django.db.models.functions import Concat
from django.db.models import Value
from datetime import date, datetime,timedelta
from easyMed import views

def home1(request):
    return render(request, 'home1.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, ('You Have Been Logged In!'))
            context = Appointment.get_context_new()
            #print("Using Authenticate views")
            return render(request, 'homeunimed.html', context)
        else:
            messages.success(request, ('Error Logging in - Please Try Again!'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def forward(request, date):
    #print(date)
    date_selected = Appointment.currentdate("Forward", date) #get the date for the context
    #print(date_selected)
    context = Appointment.get_context_new(date_selected)
    #print(context)
    return render(request, 'homeunimed.html', context)

def back(request, date):
    date_selected = Appointment.currentdate("Back", date) # get the date for the context
    context = Appointment.get_context_new(date_selected)
    print(context)
    return render(request, 'homeunimed.html', context)
