# Dao/AppointmentDao.py
from DbConnection.ConnectionDb import ConnectionDb
from datetime import date

class AppointmentDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def get_todays_appointments_for_doctor(self, doctor_id):
        q = """SELECT a.AppointmentId, a.AppointmentTime, a.TokenNumber, a.AppointmentStatus,
                      p.PatientName, p.PatientId
               FROM TblAppointment a
               JOIN TblPatient p ON a.PatientId = p.PatientId
               WHERE a.DoctorId = %s AND a.AppointmentDate = CURDATE() AND a.IsActive = 1
               ORDER BY a.AppointmentTime"""
        return self.db.fetch_all(q, (doctor_id,))\

    def get_appointment_by_id(self, appointment_id):
        q = "SELECT * FROM TblAppointment WHERE AppointmentId = %s"
        rows = self.db.fetch_all(q, (appointment_id,))
        return rows[0] if rows else None

    def create_appointment(self, appointment_date, appointment_time, token_number, patient_id, doctor_id, status='Scheduled'):
        q = """INSERT INTO TblAppointment (AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId, DoctorId, IsActive)
               VALUES (%s, %s, %s, %s, %s, %s, 1)"""
        return self.db.execute(q, (appointment_date, appointment_time, token_number, status, patient_id, doctor_id), commit=True)

    def update_status(self, appointment_id, new_status):
        q = "UPDATE TblAppointment SET AppointmentStatus = %s WHERE AppointmentId = %s"
        return self.db.execute(q, (new_status, appointment_id), commit=True)

    def get_max_token_for_date_doctor(self, appointment_date, doctor_id):
        q = "SELECT MAX(TokenNumber) as maxToken FROM TblAppointment WHERE AppointmentDate = %s AND DoctorId = %s"
        rows = self.db.fetch_all(q, (appointment_date, doctor_id))
        return rows[0]['maxToken'] if rows and rows[0]['maxToken'] is not None else 0

    def is_slot_taken(self, appointment_date, appointment_time, doctor_id):
        q = """SELECT COUNT(1) as cnt FROM TblAppointment
               WHERE AppointmentDate = %s AND AppointmentTime = %s AND DoctorId = %s AND IsActive = 1"""
        rows = self.db.fetch_all(q, (appointment_date, appointment_time, doctor_id))
        return rows[0]['cnt'] > 0
