from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from datetime import date,datetime,timedelta


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
    practice = models.ForeignKey(Practice, related_name='practice',on_delete=models.DO_NOTHING)
    name = models.ForeignKey(User, related_name ='doctor', on_delete=models.DO_NOTHING)
    selected = models.BooleanField()

    def __str__(self):
        #return (self.specialisation+" "+str(self.selected))
        return f"{self.name}"

    @staticmethod
    def get_list_doctors():
        all_doctors = User.objects.exclude(is_superuser=True).filter(doctor__isnull=False)
        all_doctors_names = all_doctors.values('first_name', 'last_name', 'id','doctor__selected')
        return all_doctors_names

    @staticmethod
    def get_selected_doctors():
        all_selected_doctors = User.objects.exclude(is_superuser=True).filter(doctor__isnull=False)
        #print(all_selected_doctors)
        #selected_doctor_pks = Doctor.objects.filter(selected=True).values('pk')
        all_selected_doctors_names = all_selected_doctors.filter(doctor__selected=True).values('first_name', 'last_name', 'id', 'doctor__selected')
        #print(all_selected_doctors_names)
        return all_selected_doctors_names

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

    #NOT USED - INITIAL IMPLEMENTATION OF APPOINTMENTS FOR A DOCTOR
    @staticmethod
    def get_appointments(doctor_id, date_selected):
        #doctor_id = doctor_id
        #date_selected = date_selected
        appointment_list = Appointment.objects.filter(start_time__year=date_selected.year,
                               start_time__month=date_selected.month,
                               start_time__day=date_selected.day).filter(doctor=doctor_id).values('start_time', 'end_time', 'patient')
        return appointment_list

    #SUPPORT METHOD TO CREATE SLOTS
    @staticmethod
    def get_daily_slots(start, end, slot, date):
         # combine start time to respective day
        dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
        slots = [dt.time()]
        # increment current time by slot till the end time
        while (dt.time() < datetime.strptime(end,"%H:%M").time()):
            dt = dt + timedelta(minutes=slot)
            dtTime = dt.time()
            slots.append(dtTime)
        return slots

    #METHOD TO CREATE SLOTS - MOVE TO ADMIN LATER AS AN ADMINSTRATIVE FUNCTION. MAY NEED TO MAKE IT SPECIFIC TO EACH DOCTOR
    @staticmethod
    def create_daily_slots():
        #Timeslot definition
        # Some Dummy values
        slot_start_time = '9:00'
        slot_end_time = '15:00'
        slot_time = 30
        slot_days = 2
        #start_date = datetime.now().date()
        start_date=date(2018,9,22)

        for i in range(slot_days):
            #date_required = datetime.now().date() + timedelta(days=1)
            date_required = start_date
            slots = Appointment.get_daily_slots(start=slot_start_time, end=slot_end_time, slot=slot_time, date=date_required)
            #print(slots)

        return slots

    #METHOD TO FIND PATIENT NAME IF DOCTOR HAS AN APPOINTMENT FOR THE GIVEN SLOT
    @staticmethod
    def get_slot_appointment(doctor_id, date_selected, slot_time):
        app_data={}
        #print(doctor_id)
        #print(date_selected)
        #print(slot_time)
        appointment_detail = Appointment.objects.filter(start_time__year=date_selected.year,
                               start_time__month=date_selected.month,
                               start_time__day=date_selected.day).filter(doctor=doctor_id).values('start_time', 'end_time', 'id')
        #print(appointment_detail)
        if appointment_detail:
            for appt in appointment_detail:
                print(appt['start_time'].time().replace(tzinfo=None))
                print(slot_time)
                print(slot_time.replace(tzinfo=None) == appt['start_time'].time().replace(tzinfo=None))
                if slot_time.replace(tzinfo=None) == appt['start_time'].time().replace(tzinfo=None):
                    app_data= User.objects.filter(id=appt['id']).values('first_name', 'last_name')
                else:
                    app_data=""
        else:
            app_data=""
            #print(app_data)
        return app_data



    @staticmethod
    def make_table(doctor_list, slots, appointment_list, doctor_numbers, slot_numbers):
        #METHOD TO CREATE A TABLE WITH ROWS AS SLOT, DOCTOR1 APPOINTMENT, DOCTOR2 APPT ETC.
        appt_list = {}

        #POPULATE REST OF TABLE WTIH SLOT AND PATIENT FULL NAME

        for i in range(0,slot_numbers):
            data=[]
            data.append(slots[i])
            for j in range(0,doctor_numbers):
                if appointment_list[j][i]:
                    #print(j,i)
                    #print(appointment_list[j][i][0]['first_name'])
                    data.append(appointment_list[j][i][0]['appointment']['patientname']['first_name'] + " " + appointment_list[j][i][0]['appointment']['patientname']['last_name'])
                else:
                    #print(j,i)
                    data.append("")
            appt_list.append(data)

        #print(appt_list)
        return appt_list

    #CREATES CONTEXT FOR THE TEMPLATE
    @staticmethod
    def get_context_new(*args):
        if not args:
            today_date = Appointment.currentdate()
        else:
            today_date = args[0]

        doctor_list = Doctor.get_list_doctors()
        selected_doctor_list = Doctor.get_selected_doctors()

        num_lists = int(selected_doctor_list.count())
        apptlists = []

        context={}

        slots = Appointment.create_daily_slots()

        #today_date = date(2018,9,22)
        context_appointment = {}
        for doctor in selected_doctor_list:
            apptlists={}
            for slot in slots:
                doctor_id = doctor['id']
                time_slot = slot
                app_data= Appointment.get_slot_appointment(doctor_id,today_date, slot)
                #print(app_data)
                apptlists['patientname']=app_data
                apptlists['slot']=slot
            context_appointment['appointment']=apptlists
            context_appontment['doctor']=doctor_id

        no_of_slots = len(slots)
        context['date']=today_date
        context['doctor_list']=doctor_list
        context['selected_doctor_list'] = selected_doctor_list
        context['appointment_list']= Appointment.make_table(selected_doctor_list, slots, context_appointment,  num_lists, no_of_slots)

        return(context)


    #Method to change the date when clicked forward or back button

    @staticmethod
    def currentdate(*args):
        if not args:
            selected_date = datetime.now() # picks today's date as default view
        else:
            currentdate = datetime.strptime(args[1], "%Y-%m-%d  %H:%M:%S.%f") #converts string to date format
            print(currentdate)
            if args[0] == "Forward":
                selected_date = currentdate + timedelta(days=1) # increment day by one
                print(selected_date)
            elif args[0] == "Back":
                selected_date = currentdate - timedelta(days=1) # reduce day by one

        return selected_date
