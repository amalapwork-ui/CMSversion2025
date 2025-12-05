# Dao/MedicineDao.py
from DbConnection.ConnectionDb import ConnectionDb

class MedicineDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def add_medicine(self, name, expiry_date, category_id):
        q = """INSERT INTO TblMedicine (MedicineName, ExpiryDate, MedicineCategoryId, IsActive)
               VALUES (%s, %s, %s, 1)"""
        return self.db.execute(q, (name, expiry_date, category_id))

    def get_medicine_by_id(self, med_id):
        q = "SELECT * FROM TblMedicine WHERE MedicineId = %s AND IsActive = 1"
        rows = self.db.fetch_all(q, (med_id,))
        return rows[0] if rows else None

    def get_all_medicines(self):
        q = "SELECT * FROM TblMedicine WHERE IsActive = 1"
        return self.db.fetch_all(q)
