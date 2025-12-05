# Models/Consultation.py
class Consultation:
    def __init__(self, consultation_id=None, symptoms=None, diagnosis=None, notes=None,
                 created_date=None, appointment_id=None, is_active=True):
        self.consultation_id = consultation_id
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.notes = notes
        self.created_date = created_date
        self.appointment_id = appointment_id
        self.is_active = is_active
