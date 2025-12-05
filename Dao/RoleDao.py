# # Dao/RoleDao.py
# from DbConnection.ConnectionDb import ConnectionDb

# class RoleDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def get_role_by_id(self, role_id):
#         q = "SELECT RoleId, RoleName, IsActive FROM TblRole WHERE RoleId = %s"
#         rows = self.db.fetch_all(q, (role_id,))
#         return rows[0] if rows else None

#     def get_role_by_name(self, role_name):
#         q = "SELECT RoleId, RoleName FROM TblRole WHERE RoleName = %s"
#         rows = self.db.fetch_all(q, (role_name,))
#         return rows[0] if rows else None



# Dao/RoleDao.py
from DbConnection.ConnectionDb import ConnectionDb

class RoleDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def create_role(self, role_name):
        q = "INSERT INTO TblRole (RoleName, IsActive) VALUES (%s, 1)"
        return self.db.execute(q, (role_name,))

    def update_role(self, role_id, role_name):
        q = "UPDATE TblRole SET RoleName = %s WHERE RoleId = %s"
        self.db.execute(q, (role_name, role_id))

    def get_all_roles(self):
        q = "SELECT * FROM TblRole"
        return self.db.fetch_all(q)

    def get_role_by_id(self, role_id):
        q = "SELECT * FROM TblRole WHERE RoleId = %s"
        rows = self.db.fetch_all(q, (role_id,))
        return rows[0] if rows else None
