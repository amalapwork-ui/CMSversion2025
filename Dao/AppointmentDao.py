# # # Dao/AppointmentDao.py
# # from DbConnection.ConnectionDb import ConnectionDb
# # from datetime import date
# # from Exceptions.Errors import ValidationError

# # class AppointmentDao:
# #     def __init__(self):
# #         self.db = ConnectionDb.get_instance()

# #     def get_todays_appointments_for_doctor(self, doctor_id):
# #         q = """SELECT a.AppointmentId, a.AppointmentTime, a.TokenNumber, a.AppointmentStatus,
# #                       p.PatientName, p.PatientId
# #                FROM TblAppointment a
# #                JOIN TblPatient p ON a.PatientId = p.PatientId
# #                WHERE a.DoctorId = %s AND a.AppointmentDate = CURDATE() AND a.IsActive = 1
# #                ORDER BY a.AppointmentTime"""
# #         return self.db.fetch_all(q, (doctor_id,))

# #     def get_appointment_by_id(self, appointment_id):
# #         q = "SELECT * FROM TblAppointment WHERE AppointmentId = %s"
# #         rows = self.db.fetch_all(q, (appointment_id,))
# #         return rows[0] if rows else None

# #     def create_appointment(self, appointment_date, appointment_time, token_number, patient_id, doctor_id, status='Scheduled'):
# #         q = """INSERT INTO TblAppointment (AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId, DoctorId, IsActive)
# #                VALUES (%s, %s, %s, %s, %s, %s, 1)"""
# #         return self.db.execute(q, (appointment_date, appointment_time, token_number, status, patient_id, doctor_id), commit=True)

# #     def update_status(self, appointment_id, new_status):
# #         q = "UPDATE TblAppointment SET AppointmentStatus = %s WHERE AppointmentId = %s"
# #         return self.db.execute(q, (new_status, appointment_id), commit=True)

# #     def get_max_token_for_date_doctor(self, appointment_date, doctor_id):
# #         q = "SELECT MAX(TokenNumber) as maxToken FROM TblAppointment WHERE AppointmentDate = %s AND DoctorId = %s"
# #         rows = self.db.fetch_all(q, (appointment_date, doctor_id))
# #         return rows[0]['maxToken'] if rows and rows[0]['maxToken'] is not None else 0

# #     def is_slot_taken(self, appointment_date, appointment_time, doctor_id):
# #         q = """SELECT COUNT(1) as cnt FROM TblAppointment
# #                WHERE AppointmentDate = %s AND AppointmentTime = %s AND DoctorId = %s AND IsActive = 1"""
# #         rows = self.db.fetch_all(q, (appointment_date, appointment_time, doctor_id))
# #         return rows[0]['cnt'] > 0

# #     def get_schedule_for_doctor(self, doctor_id):
# #         q = "SELECT * FROM TblDoctorSchedule WHERE DoctorId = %s AND IsActive = 1"
# #         rows = self.db.fetch_all(q, (doctor_id,))
# #         if not rows:
# #             raise ValidationError("No schedule found for this doctor. Please ask admin to create one.")
# #         return rows[0]


# # Dao/AppointmentDao.py
# from DbConnection.ConnectionDb import ConnectionDb
# from Exceptions.Errors import NotFoundError, DBError

# class AppointmentDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def get_schedule_for_doctor(self, doctor_id):
#         """
#         Return the schedule rows for a doctor (list). If none found, returns [].
#         Each schedule row should include: ScheduleId, DoctorId, StartTime, EndTime, SlotDuration
#         """
#         q = "SELECT ScheduleId, DoctorId, StartTime, EndTime, SlotDuration FROM TblDoctorSchedule WHERE DoctorId = %s AND IsActive = 1"
#         return self.db.fetch_all(q, (doctor_id,))
    
#     def get_todays_appointments_for_doctor(self, doctor_id):
#         q = """SELECT a.AppointmentId, a.AppointmentTime, a.TokenNumber, a.AppointmentStatus,
#                       p.PatientName, p.PatientId
#                FROM TblAppointment a
#                JOIN TblPatient p ON a.PatientId = p.PatientId
#                WHERE a.DoctorId = %s AND a.AppointmentDate = CURDATE() AND a.IsActive = 1
#                ORDER BY a.AppointmentTime"""
#         return self.db.fetch_all(q, (doctor_id,))

#     def get_appointments_for_doctor_on_date(self, doctor_id, appointment_date):
#         """
#         Return existing appointments for the doctor on the given date.
#         Each row includes AppointmentId, AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId
#         """
#         q = """SELECT AppointmentId, AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId
#                FROM TblAppointment
#                WHERE DoctorId = %s AND AppointmentDate = %s AND IsActive = 1
#                ORDER BY AppointmentTime"""
#         return self.db.fetch_all(q, (doctor_id, appointment_date))

#     def get_appointment_by_id(self, appointment_id):
#         q = "SELECT * FROM TblAppointment WHERE AppointmentId = %s"
#         rows = self.db.fetch_all(q, (appointment_id,))
#         return rows[0] if rows else None

#     def get_max_token_for_date_doctor(self, appointment_date, doctor_id):
#         q = "SELECT MAX(TokenNumber) AS maxToken FROM TblAppointment WHERE AppointmentDate = %s AND DoctorId = %s"
#         rows = self.db.fetch_all(q, (appointment_date, doctor_id))
#         if rows:
#             val = rows[0].get('maxToken')
#             return int(val) if val is not None else 0
#         return 0

#     def is_slot_taken_exact(self, doctor_id, appointment_date, appointment_time, slot_duration_minutes):
#         """
#         Checks whether there is any appointment for the same doctor on the same date
#         that is within +/- slot_duration_minutes of the requested time.
#         This prevents overlapping appointments.
#         """
#         # Use TIMESTAMPDIFF in minutes to measure difference between existing appt and requested
#         q = """
#         SELECT COUNT(1) AS cnt FROM TblAppointment a
#         WHERE a.DoctorId = %s
#           AND a.AppointmentDate = %s
#           AND a.IsActive = 1
#           AND ABS(TIMESTAMPDIFF(MINUTE,
#                CONCAT(a.AppointmentDate, ' ', a.AppointmentTime),
#                CONCAT(%s, ' ', %s)
#           )) < %s
#         """
#         rows = self.db.fetch_all(q, (doctor_id, appointment_date, appointment_date, appointment_time, slot_duration_minutes))
#         return rows[0]['cnt'] > 0

#     def create_appointment(self, appointment_date, appointment_time, token_number, patient_id, doctor_id, status='Scheduled'):
#         q = """INSERT INTO TblAppointment (AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId, DoctorId, IsActive)
#                VALUES (%s, %s, %s, %s, %s, %s, 1)"""
#         return self.db.execute(q, (appointment_date, appointment_time, token_number, status, patient_id, doctor_id), commit=True)

#     def update_status(self, appointment_id, new_status):
#         q = "UPDATE TblAppointment SET AppointmentStatus = %s WHERE AppointmentId = %s"
#         return self.db.execute(q, (new_status, appointment_id), commit=True)

# Dao/AppointmentDao.py
# from DbConnection.ConnectionDb import ConnectionDb
# from Exceptions.Errors import DBError

# class AppointmentDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def get_appointments_for_doctor_on_date(self, doctor_id, appointment_date):
#         q = """SELECT AppointmentId, AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId
#                FROM TblAppointment
#                WHERE DoctorId = %s AND AppointmentDate = %s AND IsActive = 1
#                ORDER BY AppointmentTime"""
#         return self.db.fetch_all(q, (doctor_id, appointment_date))

#     def get_appointment_by_id(self, appointment_id):
#         q = "SELECT * FROM TblAppointment WHERE AppointmentId = %s"
#         rows = self.db.fetch_all(q, (appointment_id,))
#         return rows[0] if rows else None

#     def get_max_token_for_date_doctor(self, appointment_date, doctor_id):
#         q = "SELECT MAX(TokenNumber) AS maxToken FROM TblAppointment WHERE AppointmentDate = %s AND DoctorId = %s"
#         rows = self.db.fetch_all(q, (appointment_date, doctor_id))
#         if rows and rows[0].get('maxToken') is not None:
#             return int(rows[0]['maxToken'])
#         return 0

#     def is_slot_taken_exact(self, doctor_id, appointment_date, appointment_time, slot_duration_minutes):
#         """
#         Checks whether there is any appointment for same doctor on same date that is within < slot_duration_minutes
#         in minutes from requested time. Uses TIMESTAMPDIFF to compare times (works on MySQL).
#         """
#         q = """
#         SELECT COUNT(1) AS cnt FROM TblAppointment a
#         WHERE a.DoctorId = %s
#           AND a.AppointmentDate = %s
#           AND a.IsActive = 1
#           AND ABS(TIMESTAMPDIFF(MINUTE,
#                CONCAT(a.AppointmentDate, ' ', a.AppointmentTime),
#                CONCAT(%s, ' ', %s)
#           )) < %s
#         """
#         rows = self.db.fetch_all(q, (doctor_id, appointment_date, appointment_date, appointment_time, slot_duration_minutes))
#         return rows[0]['cnt'] > 0

#     def create_appointment(self, appointment_date, appointment_time, token_number, patient_id, doctor_id, status='Scheduled'):
#         q = """INSERT INTO TblAppointment (AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId, DoctorId, IsActive)
#                VALUES (%s, %s, %s, %s, %s, %s, 1)"""
#         return self.db.execute(q, (appointment_date, appointment_time, token_number, status, patient_id, doctor_id))

#     def update_status(self, appointment_id, new_status):
#         q = "UPDATE TblAppointment SET AppointmentStatus = %s WHERE AppointmentId = %s"
#         return self.db.execute(q, (new_status, appointment_id))

# Dao/AppointmentDao.py
from DbConnection.ConnectionDb import ConnectionDb
from Exceptions.Errors import DBError
class AppointmentDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    # def get_appointments_for_doctor_on_date(self, doctor_id, appointment_date):
    #     q = """SELECT AppointmentId, AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId
    #            FROM TblAppointment
    #            WHERE DoctorId = %s AND AppointmentDate = %s AND IsActive = 1
    #            ORDER BY AppointmentTime"""
    #     return self.db.fetch_all(q, (doctor_id, appointment_date))
    def get_appointments_for_doctor_on_date(self, doctor_id, appointment_date):
        q = """
        SELECT a.AppointmentId, a.AppointmentDate, a.AppointmentTime, 
               a.TokenNumber, a.AppointmentStatus, a.PatientId,
               p.PatientName
        FROM TblAppointment a
        JOIN TblPatient p ON a.PatientId = p.PatientId
        WHERE a.DoctorId = %s AND a.AppointmentDate = %s AND a.IsActive = 1
        ORDER BY a.AppointmentTime
        """
        return self.db.fetch_all(q, (doctor_id, appointment_date))

    def get_appointment_by_id(self, appointment_id):
        q = "SELECT * FROM TblAppointment WHERE AppointmentId = %s"
        rows = self.db.fetch_all(q, (appointment_id,))
        return rows[0] if rows else None

    def get_max_token_for_date_doctor(self, appointment_date, doctor_id):
        q = "SELECT MAX(TokenNumber) AS maxToken FROM TblAppointment WHERE AppointmentDate = %s AND DoctorId = %s"
        rows = self.db.fetch_all(q, (appointment_date, doctor_id))
        if rows and rows[0].get('maxToken') is not None:
            return int(rows[0]['maxToken'])
        return 0

    def is_slot_taken_exact(self, doctor_id, appointment_date, appointment_time, slot_duration_minutes):
        q = """
        SELECT COUNT(1) AS cnt FROM TblAppointment a
        WHERE a.DoctorId = %s
          AND a.AppointmentDate = %s
          AND a.IsActive = 1
          AND ABS(TIMESTAMPDIFF(MINUTE,
               CONCAT(a.AppointmentDate, ' ', a.AppointmentTime),
               CONCAT(%s, ' ', %s)
          )) < %s
        """
        rows = self.db.fetch_all(q, (doctor_id, appointment_date, appointment_date, appointment_time, slot_duration_minutes))
        return rows[0]['cnt'] > 0

    def create_appointment(self, appointment_date, appointment_time, token_number, patient_id, doctor_id, status='Scheduled'):
        q = """INSERT INTO TblAppointment (AppointmentDate, AppointmentTime, TokenNumber, AppointmentStatus, PatientId, DoctorId, IsActive)
               VALUES (%s, %s, %s, %s, %s, %s, 1)"""
        return self.db.execute(q, (appointment_date, appointment_time, token_number, status, patient_id, doctor_id))

    def update_status(self, appointment_id, new_status):
        q = "UPDATE TblAppointment SET AppointmentStatus = %s WHERE AppointmentId = %s"
        return self.db.execute(q, (new_status, appointment_id))