from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import AppointmentForm
from datetime import date,datetime,timedelta
# Create your views here.


def newappointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        print(form)
        if form.is_valid():
            # End-time is a required field so need to add it to the form before saving.
            obj = form.save(commit=False)

            #<<TO DO>>NEED TO CHANGE THE TIME FROM 30 mins TO GLOBAL VARIABLE

            obj.end_time = obj.start_time + timedelta(minutes=30)

            obj.save()

            context = Appointment.get_context_new()
            #print("Just before HTTP views")
            return HttpResponseRedirect(reverse_lazy('homeunimed'))
        else:
            return render(request, "error.html", {"message": "Invalid Entry"})

    else:
        form = AppointmentForm()
        return render(request, 'makeappointment.html', {'form': form})
