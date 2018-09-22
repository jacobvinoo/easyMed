from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from easyMed.models import Practice, Doctor, Patient, Appointment
from django.template import Context, Template
from django.db.models.functions import Concat
from django.db.models import Value
from datetime import date
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

            appointment_context={}

            doctor_list = Doctor.get_list_doctors()

            #today_date = date.today()

            today_date = date(2018,9,10)

            for doctor in doctor_list:
                #doctor_id = doctor.values('id')
                appointments_list = Appointment.get_appointments(doctor, today_date)
                context = {'doctor': doctor, 'appointment': appointments_list}
                appointment_context.append(context)

            #context = { 'doctor_name': doctor_list}
            print(appointment_context)

            return render(request, 'homeunimed.html', appointment_context)

        else:
            messages.success(request, ('Error Logging in - Please Try Again!'))
            return redirect('login')

    else:
        return render(request, 'login.html', {})
