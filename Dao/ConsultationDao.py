# Dao/ConsultationDao.py
from DbConnection.ConnectionDb import ConnectionDb
from datetime import datetime

class ConsultationDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def insert_consultation(self, appointment_id, symptoms, diagnosis, notes):
        q = """INSERT INTO TblConsultation (Symptoms, Diagnosis, Notes, CreatedDate, AppointmentId, IsActive)
               VALUES (%s, %s, %s, NOW(), %s, 1)"""
        return self.db.execute(q, (symptoms, diagnosis, notes, appointment_id), commit=True)

    def get_consultations_by_patient(self, patient_id):
        q = """SELECT c.ConsultationId, c.Symptoms, c.Diagnosis, c.Notes, c.CreatedDate, a.AppointmentDate
               FROM TblConsultation c
               JOIN TblAppointment a ON c.AppointmentId = a.AppointmentId
               WHERE a.PatientId = %s AND c.IsActive = 1
               ORDER BY c.CreatedDate DESC"""
        return self.db.fetch_all(q, (patient_id,))
