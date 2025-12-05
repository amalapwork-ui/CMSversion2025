# Lib/LabTechLib.py
from Dao.LabTestDao import LabTestDao
from Dao.LabTestPrescriptionDao import LabTestPrescriptionDao

class LabTechLib:
    def __init__(self):
        self.lab_dao = LabTestDao()
        self.pres_dao = LabTestPrescriptionDao()

    def add_lab_test(self, name, ref_range, category_id, amount):
        return self.lab_dao.add_lab_test(name, ref_range, category_id, amount)

    def view_pending_tests(self):
        return self.pres_dao.get_pending_tests()

    def record_result(self, presc_id, value, result, remarks):
        self.pres_dao.update_result(presc_id, value, result, remarks)
