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
    practice = models.ForeignKey(Practice, related_name='doctor',on_delete=models.DO_NOTHING)
    name = models.ForeignKey(User, related_name ='doctor', on_delete=models.DO_NOTHING)
    selected = models.BooleanField()

    def __str__(self):
        return self.specialisation

    @staticmethod
    def get_list_doctors():
        all_doctors = User.objects.exclude(is_superuser=True).filter(doctor__isnull=False)
        all_doctors_names = all_doctors.values('first_name', 'last_name', 'id')
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
    def get_appointments(doctor_id, date_selected):
        #doctor_id = doctor_id
        #date_selected = date_selected
        appointment_list = Appointment.objects.filter(start_time__year=date_selected.year,
                               start_time__month=date_selected.month,
                               start_time__day=date_selected.day).filter(doctor=doctor_id).values('start_time', 'end_time', 'patient')
        return appointment_list

    @staticmethod
    def get_daily_slots(start, end, slot, date):
         # combine start time to respective day
        dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
        slots = [dt]
        # increment current time by slot till the end time
        while (dt.time() < datetime.strptime(end,"%H:%M").time()):
            dt = dt + timedelta(minutes=slot)
            slots.append(dt)
        return slots

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
                #print(appt['start_time'])
                #print(slot_time)
                #print(slot_time.replace(tzinfo=None) == appt['start_time'].replace(tzinfo=None))
                if slot_time.replace(tzinfo=None) == appt['start_time'].replace(tzinfo=None):
                    app_data= User.objects.filter(id=appt['id']).values('first_name', 'last_name')
                else:
                    app_data=""
        else:
            app_data=""
            #print(app_data)
        return app_data

    @staticmethod
    def get_context():
        context={}
        app_data_doctor=[]
        app_data=[]

        doctor_list = Doctor.get_list_doctors()
        slots = Appointment.create_daily_slots()
        today_date = date(2018,9,22)

        for doctor in doctor_list:
            for slot in slots:
                doctor_id = doctor['id']

                #time_slot = slot.time
                app_data= Appointment.get_slot_appointment(doctor_id,today_date, slot)
                print(doctor_id)
                print(app_data)
                app_data_doctor.append(app_data)

        #print(app_data_doctor)

        context['date']=today_date
        context['doctor_list']=doctor_list
        context['appointment_list']= app_data_doctor
        context['slots'] = slots
        context['no_of_slots'] = len(slots)
        context['no_of_doctors'] = len(doctor_list)
        print(context)
        return(context)

    @staticmethod
    def make_table(doctor_list, slots, appointment_list, doctor_numbers, slot_numbers):
        #METHOD TO CREATE A TABLE WITH ROWS AS SLOT, DOCTOR1 APPOINTMENT, DOCTOR2 APPT ETC.
        appt_list = []
        #header = ["Slot"]
        #data=[]
        #slots =slots
        #appointment_list = self.appointment_list
        #slot_numbers = self.slot_numbers
        #print(appointment_list)
        # GET DOCTOR FULL NAME AND ADD TO HEADER
        #doctors_all_list=[]
        #for doctor in doctor_list:
            #for item in doctor:
                #print(doctor['first_name']+" "+doctor['last_name'])
                #header.append(doctor['first_name']+" "+doctor['last_name'])
        #appt_list.append(header)
        #POPULATE REST OF TABLE WTIH SLOT AND PATIENT FULL NAME

        for i in range(0,slot_numbers):
            data=[]
            data.append(slots[i])
            for j in range(0,doctor_numbers):
                if appointment_list[j][i]:
                    print(j,i)
                    #print(appointment_list[j][i][0]['first_name'])
                    data.append(appointment_list[j][i][0]['first_name'] + " " + appointment_list[j][i][0]['last_name'])
                else:
                    print(j,i)
                    data.append("Empty")
            appt_list.append(data)

        print(appt_list)
        return appt_list

    @staticmethod
    def get_context_new():
        doctor_list = Doctor.get_list_doctors()

        num_lists = int(doctor_list.count())
        apptlists = []
        #for p in range(num_lists):
        #    apptlists.append([])

        #i=0

        context={}
        #app_data_doctor=[]
        #app_data=[]

        slots = Appointment.create_daily_slots()
        today_date = date(2018,9,22)
        context_appointment = []
        for doctor in doctor_list:
            apptlists=[]
            for slot in slots:
                doctor_id = doctor['id']
                time_slot = slot.time
                app_data= Appointment.get_slot_appointment(doctor_id,today_date, slot)
                #print(app_data)
                apptlists.append(app_data)
            context_appointment.append(apptlists)

        no_of_slots = len(slots)
        context['date']=today_date
        context['doctor_list']=doctor_list
        context['appointment_list']= Appointment.make_table(doctor_list, slots, context_appointment,  num_lists, no_of_slots)
        #context['slots'] = slots
        #context['number'] = num_lists


        #context_appt =  list(map(list, zip(*context_appointment)))
        #print(context)
        return(context)





    @staticmethod
    def get_appointment_context():
        data=[]
        context={}
        doctor_list = Doctor.get_list_doctors()
        slots = Appointment.create_daily_slots()
        #today_date = date.today()
        #<CL> Date selected. Default value of today and user can click for another date.
        today_date = date(2018,9,22)
        # create context to pass date selected, list of doctors for left pane and list of appointments for each doctor for the right pane
        for doctor in doctor_list:
            app_data={}
            doctor_id = doctor['id']
            #print(doctor_id)
            appointments_list = Appointment.get_appointments(doctor_id, today_date)
            #print(appointments_list)
            for slot in slots:
                #print(slot.time)
                if not appointments_list:
                    for appt in appointments_list:
                        if slot.time == appointments_list['start_time']:
                            app_data[doctor_id]= User.Objects.values('first_name', 'last_name', flat=True).filter(id=appt.patient)
                        else:
                            app_data[doctor_id]= ""
                else:
                    app_data[doctor_id]=""
            data.append(app_data)
        print(data)
            #context = { 'doctor_name': doctor_list}

        #----------------------------

        context['date']=today_date
        context['doctor_list']=doctor_list
        context['appointment_list']= data
        context['slots'] = slots
        return(context)
