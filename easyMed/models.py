from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Practice(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    phone = models.IntegerField()
    def __str__(self):
        return self.name

class Doctor(models.Model):
    specialisation = models.CharField(max_length=50)
    practice = models.ForeignKey(Practice, related_name='doctor',on_delete=models.DO_NOTHING)
    name = models.ForeignKey(User, related_name ='doctor', on_delete=models.DO_NOTHING)
    selected = models.BooleanField(default=False)
    def __str__(self):
        return self.specialisation


class Patient(models.Model):
    name = models.ForeignKey(User, related_name='patient', on_delete=models.DO_NOTHING)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    practice = models.ForeignKey(Practice, related_name='patient',on_delete=models.DO_NOTHING)
    primary_doctor = models.ForeignKey(Doctor, related_name='patient',on_delete=models.DO_NOTHING)


class Appointment(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, related_name='appointment',on_delete=models.DO_NOTHING)
    practice = models.ForeignKey(Practice, related_name='appointment',on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, related_name='appointment',on_delete=models.DO_NOTHING)
