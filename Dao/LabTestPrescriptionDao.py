# # Dao/LabTestPrescriptionDao.py
# from DbConnection.ConnectionDb import ConnectionDb

# class LabTestPrescriptionDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def insert_labtest_prescription(self, lab_test_id, notes, appointment_id):
#         q = """INSERT INTO TblLabTestPrescription (LabTestId, LabTestValue, Result, Remarks, CreatedDate, AppointmentId, IsActive)
#                VALUES (%s, NULL, NULL, %s, NOW(), %s, 1)"""
#         return self.db.execute(q, (lab_test_id, notes, appointment_id), commit=True)

#     def get_pending_by_doctor(self, doctor_id):
#         # fetch pending tests for appointments of this doctor
#         q = """SELECT ltp.LabTestPrescriptionId, ltest.TestName, a.AppointmentId, p.PatientName, ltp.CreatedDate
#                FROM TblLabTestPrescription ltp
#                JOIN TblLabTest ltest ON ltp.LabTestId = ltest.LabTestId
#                JOIN TblAppointment a ON ltp.AppointmentId = a.AppointmentId
#                JOIN TblPatient p ON a.PatientId = p.PatientId
#                WHERE a.DoctorId = %s AND ltp.IsActive = 1 AND (ltp.Result IS NULL OR ltp.Result = '')
#                ORDER BY ltp.CreatedDate"""
#         return self.db.fetch_all(q, (doctor_id,))

# Dao/LabTestPrescriptionDao.py
from DbConnection.ConnectionDb import ConnectionDb

class LabTestPrescriptionDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def insert_labtest_prescription(self, test_id, notes, appointment_id):
        q = """INSERT INTO TblLabTestPrescription
               (LabTestId, Remarks, CreatedDate, AppointmentId, IsActive)
               VALUES (%s, %s, NOW(), %s, 1)"""
        return self.db.execute(q, (test_id, notes, appointment_id))

    def get_pending_tests(self):
        q = """SELECT ltp.LabTestPrescriptionId, lt.TestName, p.PatientName, a.AppointmentId
               FROM TblLabTestPrescription ltp
               JOIN TblLabTest lt ON lt.LabTestId = ltp.LabTestId
               JOIN TblAppointment a ON a.AppointmentId = ltp.AppointmentId
               JOIN TblPatient p ON p.PatientId = a.PatientId
               WHERE ltp.Result IS NULL OR ltp.Result = '' """
        return self.db.fetch_all(q)

    def update_result(self, presc_id, value, result, remarks):
        q = """UPDATE TblLabTestPrescription
               SET LabTestValue = %s, Result = %s, Remarks = %s
               WHERE LabTestPrescriptionId = %s"""
        self.db.execute(q, (value, result, remarks, presc_id))
