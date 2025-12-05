# Models/Appointment.py
class Appointment:
    def __init__(self, appointment_id=None, appointment_date=None, appointment_time=None,
                 token_number=None, appointment_status=None, patient_id=None, doctor_id=None, is_active=True):
        self.appointment_id = appointment_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.token_number = token_number
        self.appointment_status = appointment_status
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.is_active = is_active
