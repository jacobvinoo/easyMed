from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from datetime import date


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

    @staticmethod
    def get_list_doctors():
        all_doctors = User.objects.exclude(is_superuser=True).filter(doctor__isnull=False)
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
    slots = ['8:00 AM']

    #@staticmethod
    #def filter_by_date(date):
    #    return Appointment.filter(start_time__year=date.year,
    #                      start_time__month=date.month,
    #                      start_time__day=date.day)

    @staticmethod
    def get_appointments(doctor, date_selected):
        #doctor_id = doctor_id
        #date_selected = date_selected
        appointment_list = Appointment.objects.filter(start_time__year=date_selected.year,
                               start_time__month=date_selected.month,
                               start_time__day=date_selected.day).filter(doctor.)
        return appointment_list
