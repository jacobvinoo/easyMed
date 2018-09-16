from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager



# Create your models here.
#class DoctorManager(models.Manager):

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
    selected = models.BooleanField()

    def __str__(self):
        return self.specialisation

    def get_list_doctors(self):
        all_doctors = User.objects.exclude(pk=1).filter(doctor__isnull=False)
        all_doctors_names = all_doctors.values_list('first_name', 'last_name', 'id')
        return all_doctors_names

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
