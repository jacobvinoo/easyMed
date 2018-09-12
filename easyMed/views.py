from django.http import HttpResponse
from django.shortcuts import render
from .models import Practice, Doctor, Patient, Appointment

# Create your views here.

def homeunimed(request):
    appointments = Appointment.objects.all()
    appointment_list = list()

    for appointment in appoinments:
        appointments_list.append(appointment.start_time)

    response_html = '<br>'.join(appointments_list)

    return HttpResponse(response_html)


def login_context():
    login_practice = "Unimed" # Change - get practice from the list selected
    login_doctors = User.objects.exclude(pk=1).values_list('last_name', 'first_name').filter(doctor__isnull=False).filter(practice=login_practice)
    return login_doctors
