# Dao/DoctorDao.py
from DbConnection.ConnectionDb import ConnectionDb

class DoctorDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def get_doctor_by_staff_id(self, staff_id):
        q = "SELECT DoctorId, StaffId, SpecializationId, ConsultationFee, IsActive FROM TblDoctor WHERE StaffId = %s AND IsActive = 1"
        rows = self.db.fetch_all(q, (staff_id,))
        return rows[0] if rows else None

    def get_doctor_by_id(self, doctor_id):
        q = "SELECT DoctorId, StaffId, SpecializationId, ConsultationFee, IsActive FROM TblDoctor WHERE DoctorId = %s"
        rows = self.db.fetch_all(q, (doctor_id,))
        return rows[0] if rows else None

    def get_schedule(self, doctor_id):
        q = "SELECT ScheduleId, DoctorId, StartTime, EndTime, SlotDuration FROM TblDoctorSchedule WHERE DoctorId = %s"
        return self.db.fetch_all(q, (doctor_id,))

    def create_doctor(self, staff_id, specialization_id, fee):
        q = """
        INSERT INTO TblDoctor 
        (StaffId, SpecializationId, ConsultationFee, IsActive)
        VALUES (%s, %s, %s, 1)
        """
        return self.db.execute(q, (staff_id, specialization_id, fee))

    def update_doctor(self, doctor_id, specialization_id, fee):
        q = """
        UPDATE TblDoctor SET 
            SpecializationId = %s,
            ConsultationFee = %s
        WHERE DoctorId = %s
        """
        self.db.execute(q, (specialization_id, fee, doctor_id))

    def deactivate_doctor(self, doctor_id):
        q = "UPDATE TblDoctor SET IsActive = 0 WHERE DoctorId = %s"
        self.db.execute(q, (doctor_id,))

    def reactivate_doctor(self, doctor_id):
        q = "UPDATE TblDoctor SET IsActive = 1 WHERE DoctorId = %s"
        self.db.execute(q, (doctor_id,))
