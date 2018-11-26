from django import forms
from easyMed.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields= ["start_time", "doctor", "patient"]
