# Models/Doctor.py

class Doctor:
    def __init__(self, doctor_id=None, staff_id=None, specialization_id=None, consultation_fee=0.0, is_active=True):
        self.doctor_id = doctor_id
        self.staff_id = staff_id
        self.specialization_id = specialization_id
        self.consultation_fee = consultation_fee
        self.is_active = is_active
