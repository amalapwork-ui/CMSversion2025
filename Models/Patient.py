# Models/Patient.py
class Patient:
    def __init__(self, patient_id=None, patient_name=None, date_of_birth=None, gender=None,
                 mobile_number=None, address=None, membership_id=None, is_active=True):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.mobile_number = mobile_number
        self.address = address
        self.membership_id = membership_id
        self.is_active = is_active
