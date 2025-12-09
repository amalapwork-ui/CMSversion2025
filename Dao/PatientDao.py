# Dao/PatientDao.py
from DbConnection.ConnectionDb import ConnectionDb

class PatientDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def create_patient(self, patient_name, dob, gender, mobile_number, address):
        q = """INSERT INTO TblPatient (PatientName, DateOfBirth, Gender, MobileNumber, Address, IsActive)
               VALUES (%s, %s, %s, %s, %s, 1)"""
        return self.db.execute(q, (patient_name, dob, gender, mobile_number, address), commit=True)

    def get_patient_by_id(self, patient_id):
        q = "SELECT PatientId, PatientName, DateOfBirth, Gender, MobileNumber, Address, IsActive FROM TblPatient WHERE PatientId = %s"
        rows = self.db.fetch_all(q, (patient_id,))
        return rows[0] if rows else None

    def find_patient_by_mobile(self, mobile_number):
        q = "SELECT PatientId, PatientName, MobileNumber FROM TblPatient WHERE MobileNumber = %s"
        rows = self.db.fetch_all(q, (mobile_number,))
        return rows[0] if rows else None
    
