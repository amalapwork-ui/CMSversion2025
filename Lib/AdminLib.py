# Lib/AdminLib.py
from Dao.StaffDao import StaffDao
from Dao.RoleDao import RoleDao
from Dao.DoctorDao import DoctorDao
from Dao.SpecializationDao import SpecializationDao

class AdminLib:
    def __init__(self):
        self.staff_dao = StaffDao()
        self.role_dao = RoleDao()
        self.doctor_dao = DoctorDao()
        self.spec_dao = SpecializationDao()

    # ----------- STAFF MANAGEMENT ------------
    def add_staff(self, fullname, gender, joining, mobile, username, password, role_id):
        return self.staff_dao.create_staff(fullname, gender, joining, mobile, username, password, role_id)

    def update_staff(self, staff_id, fullname, gender, mobile, role_id):
        self.staff_dao.update_staff(staff_id, fullname, gender, mobile, role_id)

    def deactivate_staff(self, staff_id):
        self.staff_dao.deactivate_staff(staff_id)

    def reactivate_staff(self, staff_id):
        self.staff_dao.reactivate_staff(staff_id)

    def get_all_staff(self):
        return self.staff_dao.get_all_staff()

    # ----------- ROLE MANAGEMENT ------------
    def add_role(self, role_name):
        return self.role_dao.create_role(role_name)

    def update_role(self, role_id, name):
        self.role_dao.update_role(role_id, name)

    def get_roles(self):
        return self.role_dao.get_all_roles()

    # ----------- SPECIALIZATION MANAGEMENT ------------
    def add_specialization(self, name):
        return self.spec_dao.add_specialization(name)

    def update_specialization(self, spec_id, name):
        self.spec_dao.update_specialization(spec_id, name)

    def deactivate_specialization(self, spec_id):
        self.spec_dao.deactivate_specialization(spec_id)

    def reactivate_specialization(self, spec_id):
        self.spec_dao.reactivate_specialization(spec_id)

    def get_all_specializations(self):
        return self.spec_dao.get_all_specializations()

    # ----------- DOCTOR MANAGEMENT ------------
    def create_doctor_profile(self, staff_id, specialization_id, fee):
        return self.doctor_dao.create_doctor(staff_id, specialization_id, fee)

    def update_doctor(self, doctor_id, specialization_id, fee):
        self.doctor_dao.update_doctor(doctor_id, specialization_id, fee)

    def deactivate_doctor(self, doctor_id):
        self.doctor_dao.deactivate_doctor(doctor_id)

    def reactivate_doctor(self, doctor_id):
        self.doctor_dao.reactivate_doctor(doctor_id)
