# # Dao/DoctorDao.py
# from DbConnection.ConnectionDb import ConnectionDb
# from Exceptions.Errors import DBError, ValidationError

# class DoctorDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def get_doctor_by_staff_id(self, staff_id):
#         q = "SELECT DoctorId, StaffId, SpecializationId, ConsultationFee, IsActive FROM TblDoctor WHERE StaffId = %s AND IsActive = 1"
#         rows = self.db.fetch_all(q, (staff_id,))
#         return rows[0] if rows else None

#     def get_doctor_by_id(self, doctor_id):
#         q = "SELECT DoctorId, StaffId, SpecializationId, ConsultationFee, IsActive FROM TblDoctor WHERE DoctorId = %s"
#         rows = self.db.fetch_all(q, (doctor_id,))
#         return rows[0] if rows else None

#     def get_schedule(self, doctor_id):
#         q = "SELECT ScheduleId, DoctorId, StartTime, EndTime, SlotDuration FROM TblDoctorSchedule WHERE DoctorId = %s"
#         return self.db.fetch_all(q, (doctor_id,))

#     # def create_doctor(self, staff_id, specialization_id, fee):
#     #     q = """
#     #     INSERT INTO TblDoctor 
#     #     (StaffId, SpecializationId, ConsultationFee, IsActive)
#     #     VALUES (%s, %s, %s, 1)
#     #     """
#     #     return self.db.execute(q, (staff_id, specialization_id, fee))

    
#     def create_doctor(self, staff_id, specialization_id, fee):
#         if self.check_doctor_exists_for_staff(staff_id):
#             raise ValidationError("A doctor profile already exists for this staff member.")

#         q = """
#         INSERT INTO TblDoctor (StaffId, SpecializationId, ConsultationFee, IsActive)
#         VALUES (%s, %s, %s, 1)
#         """
#         return self.db.execute(q, (staff_id, specialization_id, fee))

#     # def update_doctor(self, doctor_id, specialization_id, fee):
#     #     q = """
#     #     UPDATE TblDoctor SET 
#     #         SpecializationId = %s,
#     #         ConsultationFee = %s
#     #     WHERE DoctorId = %s
#     #     """
#     #     self.db.execute(q, (specialization_id, fee, doctor_id))
#     def update_doctor(self, doctor_id, specialization_id, fee):
#         q = """
#             UPDATE TblDoctor SET 
#                 SpecializationId = %s,
#                 ConsultationFee = %s
#             WHERE DoctorId = %s
#         """
#         try:
#             self.db.execute(q, (specialization_id, fee, doctor_id))
#         except DBError as e:
#             # Handle foreign key constraint failure
#             if "foreign key constraint fails" in str(e).lower():
#                 raise ValidationError("Invalid Specialization ID. Please choose a valid specialization.")
#             raise

#     def deactivate_doctor(self, doctor_id):
#         q = "UPDATE TblDoctor SET IsActive = 0 WHERE DoctorId = %s"
#         self.db.execute(q, (doctor_id,))

#     def reactivate_doctor(self, doctor_id):
#         q = "UPDATE TblDoctor SET IsActive = 1 WHERE DoctorId = %s"
#         self.db.execute(q, (doctor_id,))
    
#     def check_doctor_exists_for_staff(self, staff_id):
#         q = "SELECT DoctorId FROM TblDoctor WHERE StaffId = %s"
#         rows = self.db.fetch_all(q, (staff_id,))
#         return len(rows) > 0

# Dao/DoctorDao.py
from DbConnection.ConnectionDb import ConnectionDb
from Exceptions.Errors import DBError, NotFoundError, ValidationError

class DoctorDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    # ----- doctor basic -----
    def get_doctor_by_id(self, doctor_id):
        q = "SELECT DoctorId, StaffId, SpecializationId, ConsultationFee, IsActive FROM TblDoctor WHERE DoctorId = %s"
        rows = self.db.fetch_all(q, (doctor_id,))
        return rows[0] if rows else None

    def check_doctor_exists_for_staff(self, staff_id):
        q = "SELECT DoctorId FROM TblDoctor WHERE StaffId = %s"
        rows = self.db.fetch_all(q, (staff_id,))
        return len(rows) > 0

    def create_doctor(self, staff_id, specialization_id, fee):
        if self.check_doctor_exists_for_staff(staff_id):
            raise ValidationError("A doctor profile already exists for this staff member.")
        q = "INSERT INTO TblDoctor (StaffId, SpecializationId, ConsultationFee, IsActive) VALUES (%s, %s, %s, 1)"
        return self.db.execute(q, (staff_id, specialization_id, fee))

    def update_doctor(self, doctor_id, specialization_id, fee):
        q = "UPDATE TblDoctor SET SpecializationId = %s, ConsultationFee = %s WHERE DoctorId = %s"
        try:
            return self.db.execute(q, (specialization_id, fee, doctor_id))
        except DBError as e:
            if "foreign key constraint" in str(e).lower():
                raise ValidationError("Invalid Specialization ID. Please choose a valid specialization.")
            raise

    # ----- schedule related -----
    def add_schedule(self, doctor_id, start_time, end_time, slot_duration_minutes, is_active=1):
        """
        Inserts a schedule row for the doctor.
        start_time/end_time must be strings 'HH:MM:SS' or time objects handled by DB driver.
        """
        # validate doctor exists
        doc = self.get_doctor_by_id(doctor_id)
        if not doc:
            raise NotFoundError("Doctor not found.")

        q = """INSERT INTO TblDoctorSchedule (DoctorId, StartTime, EndTime, SlotDuration, IsActive)
               VALUES (%s, %s, %s, %s, %s)"""
        return self.db.execute(q, (doctor_id, start_time, end_time, slot_duration_minutes, is_active))

    def update_schedule(self, schedule_id, start_time, end_time, slot_duration_minutes, is_active=1):
        q = """UPDATE TblDoctorSchedule SET StartTime=%s, EndTime=%s, SlotDuration=%s, IsActive=%s WHERE ScheduleId=%s"""
        return self.db.execute(q, (start_time, end_time, slot_duration_minutes, is_active, schedule_id))

    def delete_schedule(self, schedule_id):
        # soft delete
        q = "UPDATE TblDoctorSchedule SET IsActive = 0 WHERE ScheduleId = %s"
        return self.db.execute(q, (schedule_id,))

    def get_schedules_for_doctor(self, doctor_id):
        q = "SELECT ScheduleId, DoctorId, StartTime, EndTime, SlotDuration, IsActive FROM TblDoctorSchedule WHERE DoctorId = %s ORDER BY StartTime"
        return self.db.fetch_all(q, (doctor_id,))
    
    def deactivate_doctor(self, doctor_id):
        q = "UPDATE TblDoctor SET IsActive = 0 WHERE DoctorId = %s"
        self.db.execute(q, (doctor_id,))

    def reactivate_doctor(self, doctor_id):
        q = "UPDATE TblDoctor SET IsActive = 1 WHERE DoctorId = %s"
        self.db.execute(q, (doctor_id,))

    def get_all_doctors_detailed(self):
        """Fetches Doctor details including Name and Specialization text."""
        q = """
        SELECT d.DoctorId, s.FullName, sp.SpecializationName, d.ConsultationFee, d.IsActive
        FROM TblDoctor d
        JOIN TblStaff s ON d.StaffId = s.StaffId
        JOIN TblSpecialization sp ON d.SpecializationId = sp.SpecializationId
        ORDER BY d.DoctorId
        """
        return self.db.fetch_all(q)