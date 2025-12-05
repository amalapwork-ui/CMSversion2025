# Dao/SpecializationDao.py
from DbConnection.ConnectionDb import ConnectionDb

class SpecializationDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def add_specialization(self, name):
        q = "INSERT INTO TblSpecialization (SpecializationName, IsActive) VALUES (%s, 1)"
        return self.db.execute(q, (name,))

    def update_specialization(self, spec_id, name):
        q = "UPDATE TblSpecialization SET SpecializationName = %s WHERE SpecializationId = %s"
        self.db.execute(q, (name, spec_id))

    def deactivate_specialization(self, spec_id):
        q = "UPDATE TblSpecialization SET IsActive = 0 WHERE SpecializationId = %s"
        self.db.execute(q, (spec_id,))

    def reactivate_specialization(self, spec_id):
        q = "UPDATE TblSpecialization SET IsActive = 1 WHERE SpecializationId = %s"
        self.db.execute(q, (spec_id,))

    def get_all_specializations(self):
        q = "SELECT * FROM TblSpecialization"
        return self.db.fetch_all(q)
