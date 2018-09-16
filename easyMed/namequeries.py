    def _login_context():
        login_practice = "Unimed" # Change - get practice from the list selected
        doctors = User.objects.exclude(pk=1).values_list('last_name', 'first_name', 'id').filter(doctor__isnull=False)
        print(doctors)
        doctors_list = doctors.doctor
        print(doctors_list)
        return doctors_list

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
