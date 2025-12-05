# # Dao/StaffDao.py
# from DbConnection.ConnectionDb import ConnectionDb

# class StaffDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def validate_login(self, username, password):
#         """
#         Return staff record dictionary including RoleId and StaffId if credentials match.
#         Also attempt to return DoctorId if this staff has a doctor profile (join).
#         """
#         q = """
#         SELECT s.StaffId, s.FullName, s.UserName, s.RoleId, s.IsActive,
#                d.DoctorId
#         FROM TblStaff s
#         LEFT JOIN TblDoctor d ON d.StaffId = s.StaffId
#         WHERE s.UserName = %s AND s.Password = %s AND s.IsActive = 1
#         LIMIT 1
#         """
#         rows = self.db.fetch_all(q, (username, password))
#         return rows[0] if rows else None

#     def get_staff_by_id(self, staff_id):
#         q = "SELECT StaffId, FullName, UserName, RoleId, IsActive FROM TblStaff WHERE StaffId = %s"
#         rows = self.db.fetch_all(q, (staff_id,))
#         return rows[0] if rows else None

#     def create_staff(self, full_name, gender, joining_date, mobile_number, username, password, role_id):
#         q = """INSERT INTO TblStaff (FullName, Gender, JoiningDate, MobileNumber, UserName, Password, RoleId, IsActive)
#                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)"""
#         return self.db.execute(q, (full_name, gender, joining_date, mobile_number, username, password, role_id), commit=True)


# Dao/StaffDao.py
from DbConnection.ConnectionDb import ConnectionDb

class StaffDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def validate_login(self, username, password):
        q = """
        SELECT s.StaffId, s.FullName, s.UserName, s.RoleId, s.IsActive,
               d.DoctorId
        FROM TblStaff s
        LEFT JOIN TblDoctor d ON d.StaffId = s.StaffId
        WHERE s.UserName = %s AND s.Password = %s AND s.IsActive = 1
        LIMIT 1
        """
        rows = self.db.fetch_all(q, (username, password))
        return rows[0] if rows else None

    def create_staff(self, fullname, gender, joining_date, mobile, username, password, role_id):
        q = """
        INSERT INTO TblStaff 
        (FullName, Gender, JoiningDate, MobileNumber, UserName, Password, RoleId, IsActive)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """
        return self.db.execute(q, (fullname, gender, joining_date, mobile, username, password, role_id))

    def update_staff(self, staff_id, fullname, gender, mobile, role_id):
        q = """
        UPDATE TblStaff SET 
            FullName = %s,
            Gender = %s,
            MobileNumber = %s,
            RoleId = %s
        WHERE StaffId = %s
        """
        self.db.execute(q, (fullname, gender, mobile, role_id, staff_id))

    def deactivate_staff(self, staff_id):
        q = "UPDATE TblStaff SET IsActive = 0 WHERE StaffId = %s"
        self.db.execute(q, (staff_id,))

    def reactivate_staff(self, staff_id):
        q = "UPDATE TblStaff SET IsActive = 1 WHERE StaffId = %s"
        self.db.execute(q, (staff_id,))

    def get_all_staff(self):
        q = "SELECT * FROM TblStaff"
        return self.db.fetch_all(q)

    def get_staff_by_id(self, staff_id):
        q = "SELECT * FROM TblStaff WHERE StaffId = %s"
        rows = self.db.fetch_all(q, (staff_id,))
        return rows[0] if rows else None
