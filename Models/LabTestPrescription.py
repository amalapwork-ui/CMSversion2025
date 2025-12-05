# Models/LabTestPrescription.py
class LabTestPrescription:
    def __init__(self, lab_test_prescription_id=None, lab_test_id=None, lab_test_value=None,
                 result=None, remarks=None, created_date=None, appointment_id=None, is_active=True):
        self.lab_test_prescription_id = lab_test_prescription_id
        self.lab_test_id = lab_test_id
        self.lab_test_value = lab_test_value
        self.result = result
        self.remarks = remarks
        self.created_date = created_date
        self.appointment_id = appointment_id
        self.is_active = is_active
