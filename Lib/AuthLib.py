# Lib/AuthLib.py
from Dao.StaffDao import StaffDao
from Dao.RoleDao import RoleDao

class AuthLib:
    def __init__(self):
        self.staff_dao = StaffDao()
        self.role_dao = RoleDao()

    def login(self, username, password):
        staff = self.staff_dao.validate_login(username, password)
        if not staff:
            return None
        role = self.role_dao.get_role_by_id(staff['RoleId'])
        session = {
            'staff_id': staff['StaffId'],
            'full_name': staff['FullName'],
            'role_id': staff['RoleId'],
            'role_name': role['RoleName'] if role else None,
            'doctor_id': staff.get('DoctorId')  # may be None
        }
        return session
