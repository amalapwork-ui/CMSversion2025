# Lib/PharmacistLib.py
from Dao.MedicineDao import MedicineDao
from Dao.MedicineStockDao import MedicineStockDao
from Dao.PrescriptionDao import PrescriptionDao

class PharmacistLib:
    def __init__(self):
        self.med_dao = MedicineDao()
        self.stock_dao = MedicineStockDao()
        self.prescription_dao = PrescriptionDao()

    def add_new_medicine(self, name, expiry_date):
        return self.med_dao.add_medicine(name, expiry_date)

    def update_stock(self, med_id, batch, qty, expiry):
        return self.stock_dao.add_stock(med_id, batch, qty, expiry)

    def view_expired_stock(self):
        return self.stock_dao.get_expired()

    def remove_expired(self, stock_id):
        self.stock_dao.remove_stock(stock_id)

    def dispense_medicines(self, appointment_id):
        meds = self.prescription_dao.get_prescriptions_by_appointment(appointment_id)
        if not meds:
            raise ValueError("No medicines prescribed.")

        for m in meds:
            med_id = m['MedicinePrescriptionId']
            # assume quantity 1 for each prescription
            self.stock_dao.update_stock_after_dispense(med_id, 1)

        return meds

    def verify_prescription(self, appointment_id):
        meds = self.prescription_dao.get_prescriptions_by_appointment(appointment_id)
        return meds
