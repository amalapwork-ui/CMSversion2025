# # Dao/MedicineStockDao.py
# from DbConnection.ConnectionDb import ConnectionDb
# from datetime import datetime

# class MedicineStockDao:
#     def __init__(self):
#         self.db = ConnectionDb.get_instance()

#     def add_stock(self, med_id, batch_no, qty, expiry):
#         q = """INSERT INTO TblMedicineStock 
#                (MedicineId, BatchNo, StockInHand, ExpiryDate, CreateDate, IsActive)
#                VALUES (%s, %s, %s, %s, NOW(), 1)"""
#         return self.db.execute(q, (med_id, batch_no, qty, expiry))
         
#     def update_stock_after_dispense(self, med_id, qty):
#         """Deduct qty from earliest expiry first (FIFO)."""
#         select_q = """SELECT * FROM TblMedicineStock 
#                       WHERE MedicineId = %s AND StockInHand > 0 
#                       ORDER BY ExpiryDate ASC"""
#         stock_rows = self.db.fetch_all(select_q, (med_id,))

#         remaining_qty = qty

#         for s in stock_rows:
#             if remaining_qty <= 0:
#                 break
#             deduct = min(s['StockInHand'], remaining_qty)
#             update_q = """UPDATE TblMedicineStock 
#                           SET StockInHand = StockInHand - %s 
#                           WHERE MedicineStockId = %s"""
#             self.db.execute(update_q, (deduct, s['MedicineStockId']))
#             remaining_qty -= deduct

#     def get_expired(self):
#         q = """SELECT * FROM TblMedicineStock 
#                WHERE ExpiryDate < CURDATE() AND IsActive = 1"""
#         return self.db.fetch_all(q)

#     def remove_stock(self, stock_id):
#         q = "UPDATE TblMedicineStock SET IsActive = 0 WHERE MedicineStockId = %s"
#         self.db.execute(q, (stock_id,))

# Dao/MedicineStockDao.py
from DbConnection.ConnectionDb import ConnectionDb
from datetime import datetime


class MedicineStockDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def add_stock(self, med_id, batch_no, qty, expiry):
        # FIX: Changed 'CreateDate' to 'CreatedDate' to match your database
        q = """INSERT INTO TblMedicineStock 
               (MedicineId, BatchNo, StockInHand, ExpiryDate, CreatedDate, IsActive)
               VALUES (%s, %s, %s, %s, NOW(), 1)"""
        return self.db.execute(q, (med_id, batch_no, qty, expiry))
         
    def update_stock_after_dispense(self, med_id, qty):
        """Deduct qty from earliest expiry first (FIFO)."""
        select_q = """SELECT * FROM TblMedicineStock 
                      WHERE MedicineId = %s AND StockInHand > 0 
                      ORDER BY ExpiryDate ASC"""
        stock_rows = self.db.fetch_all(select_q, (med_id,))

        remaining_qty = qty

        for s in stock_rows:
            if remaining_qty <= 0:
                break
            # Calculate how much to take from this specific batch
            deduct = min(s['StockInHand'], remaining_qty)
            
            update_q = """UPDATE TblMedicineStock 
                          SET StockInHand = StockInHand - %s 
                          WHERE MedicineStockId = %s"""
            self.db.execute(update_q, (deduct, s['MedicineStockId']))
            
            remaining_qty -= deduct

    def get_expired(self):
        q = """SELECT * FROM TblMedicineStock 
               WHERE ExpiryDate < CURDATE() AND IsActive = 1"""
        return self.db.fetch_all(q)

    def remove_stock(self, stock_id):
        q = "UPDATE TblMedicineStock SET IsActive = 0 WHERE MedicineStockId = %s"
        self.db.execute(q, (stock_id,))