from django.contrib import admin

# Register your models here.
from .models import Practice, Doctor, Patient, Appointment

admin.site.register(Practice)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
