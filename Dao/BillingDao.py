# Dao/BillingDao.py
from DbConnection.ConnectionDb import ConnectionDb

class BillingDao:
    def __init__(self):
        self.db = ConnectionDb.get_instance()

    def create_billing(self, appointment_id, consultation_fee, medicine_charges, lab_charges, total_amount, payment_status='Paid'):
        q = """INSERT INTO TblBilling (AppointmentId, ConsultationFee, MedicineCharges, LabCharges, TotalAmount, PaymentStatus, CreatedDate, IsActive)
               VALUES (%s, %s, %s, %s, %s, %s, NOW(), 1)"""
        return self.db.execute(q, (appointment_id, consultation_fee, medicine_charges, lab_charges, total_amount, payment_status), commit=True)

    def compute_consultation_fee(self, appointment_id):
        # fetch doctor id from appointment then doctor fee
        q = """SELECT d.ConsultationFee
               FROM TblAppointment a
               JOIN TblDoctor d ON a.DoctorId = d.DoctorId
               WHERE a.AppointmentId = %s"""
        rows = self.db.fetch_all(q, (appointment_id,))
        return float(rows[0]['ConsultationFee']) if rows else 0.0

    def compute_lab_charges(self, appointment_id):
        q = """SELECT IFNULL(SUM(lt.Amount),0) as lab_total
               FROM TblLabTestPrescription ltp
               JOIN TblLabTest lt ON ltp.LabTestId = lt.LabTestId
               WHERE ltp.AppointmentId = %s AND ltp.IsActive = 1"""
        rows = self.db.fetch_all(q, (appointment_id,))
        return float(rows[0]['lab_total']) if rows else 0.0

    def compute_medicine_charges(self, appointment_id):
        """
        If TblMedicine has a price/amount column, sum it. Otherwise returns 0.
        This query assumes TblMedicine may have 'Amount' or 'Price'. Try both.
        """
        # try Amount
        q1 = """SELECT IFNULL(SUM(m.Amount),0) as med_total
                FROM TblMedicinePrescription mp
                JOIN TblMedicine m ON mp.MedicineId = m.MedicineId
                WHERE mp.AppointmentId = %s AND mp.IsActive = 1"""
        try:
            rows = self.db.fetch_all(q1, (appointment_id,))
            return float(rows[0]['med_total']) if rows else 0.0
        except Exception:
            # fallback: return 0 if column missing
            return 0.0
