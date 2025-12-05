# Dao/LabTestDao.py
from DbConnection.ConnectionDb import ConnectionDb

class LabTestDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def add_lab_test(self, test_name, reference_range, category_id, amount):
        q = """INSERT INTO TblLabTest (TestName, ReferenceRange, LabTestCategoryId, Amount, IsActive)
               VALUES (%s, %s, %s, %s, 1)"""
        return self.db.execute(q, (test_name, reference_range, category_id, amount))

    def get_all_tests(self):
        q = "SELECT * FROM TblLabTest WHERE IsActive = 1"
        return self.db.fetch_all(q)

    def get_test_by_id(self, test_id):
        q = "SELECT * FROM TblLabTest WHERE LabTestId = %s"
        rows = self.db.fetch_all(q, (test_id,))
        return rows[0] if rows else None
