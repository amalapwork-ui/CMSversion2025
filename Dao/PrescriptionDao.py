# Dao/PrescriptionDao.py
from DbConnection.ConnectionDb import ConnectionDb

class PrescriptionDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def insert_medicine_prescription(self, medicine_id, dosage, frequency, duration, appointment_id):
        q = """INSERT INTO TblMedicinePrescription (MedicineId, Dosage, Frequency, Duration, AppointmentId, IsActive)
               VALUES (%s, %s, %s, %s, %s, 1)"""
        return self.db.execute(q, (medicine_id, dosage, frequency, duration, appointment_id), commit=True)

    def get_prescriptions_by_appointment(self, appointment_id):
        q = """SELECT mp.MedicinePrescriptionId, m.MedicineName, mp.Dosage, mp.Frequency, mp.Duration
               FROM TblMedicinePrescription mp
               JOIN TblMedicine m ON mp.MedicineId = m.MedicineId
               WHERE mp.AppointmentId = %s AND mp.IsActive = 1"""
        return self.db.fetch_all(q, (appointment_id,))
