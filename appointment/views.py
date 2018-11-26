from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import AppointmentForm
# Create your views here.


def newappointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()

            context = Appointment.get_context_new()
            #print("Just before HTTP views")
            return HttpResponseRedirect(reverse_lazy('homeunimed'))
        else:
            return render(request, "error.html", {"message": "Invalid Entry"})

    else:
        form = AppointmentForm()
        return render(request, 'makeappointment.html', {'form': form})
