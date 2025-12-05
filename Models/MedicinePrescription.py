# Models/MedicinePrescription.py
class MedicinePrescription:
    def __init__(self, medicine_prescription_id=None, medicine_id=None, dosage=None,
                 frequency=None, duration=None, appointment_id=None, is_active=True):
        self.medicine_prescription_id = medicine_prescription_id
        self.medicine_id = medicine_id
        self.dosage = dosage
        self.frequency = frequency
        self.duration = duration
        self.appointment_id = appointment_id
        self.is_active = is_active
