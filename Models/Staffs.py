# Models/Staffs.py
class Staff:
    def __init__(self, staff_id=None, full_name=None, gender=None, joining_date=None,
                 mobile_number=None, username=None, password=None, role_id=None, is_active=True):
        self.staff_id = staff_id
        self.full_name = full_name
        self.gender = gender
        self.joining_date = joining_date
        self.mobile_number = mobile_number
        self.username = username
        self.password = password
        self.role_id = role_id
        self.is_active = is_active
