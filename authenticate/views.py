from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from easyMed.models import Practice, Doctor, Patient, Appointment
from django.template import Context, Template
from django.db.models.functions import Concat
from django.db.models import Value

def home1(request):
    return render(request, 'home1.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You Have Been Logged In!'))
            doctor_list = User.objects.exclude(pk=1).filter(doctor_isnull=False).get_full_name()
            print(doctor_list)
            all_doctors = list(User.objects.exclude(pk=1).filter(doctor__isnull=False).values_list('first_name', 'last_name').annotate(full_name=Concat('first_name', Value(' '), 'last_name')))
            #doctors_firstname =   all_doctors.values_list('first_name','last_name'))
            #t_doctors = list(zip(*all_doctors))
            #doctors_lastname = all_doctors.values_list('last_name')
            #doctor_list = zip(doctors_firstname, doctors_lastname)
            context = { 'doctor_name': all_doctors}
            print(context)
            #            ' doctor_secondname': all_doctors_lastname
            #            }

                #all_appointments = Appointment.objects.all()
            print(all_doctors)
            #return redirect('home')
            return render(request, 'homeunimed.html', context)
            # {'doctors_firstname':doctors_firstname, 'doctors_lastname': doctors_lastname})
        else:
            messages.success(request, ('Error Logging in - Please Try Again!'))
            return redirect('login')

    else:
        return render(request, 'login.html', {})
