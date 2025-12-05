# Lib/ReceptionLib.py
from Dao.PatientDao import PatientDao
from Dao.DoctorDao import DoctorDao
from Dao.AppointmentDao import AppointmentDao
from Dao.BillingDao import BillingDao
from datetime import datetime, timedelta, time
from Validation.AppointmentValidation import validate_date_str, validate_time_str
from Exceptions.Errors import ValidationError, ConflictError, NotFoundError

class ReceptionLib:
    def __init__(self):
        self.patient_dao = PatientDao()
        self.doctor_dao = DoctorDao()
        self.appointment_dao = AppointmentDao()
        self.billing_dao = BillingDao()

    def register_patient(self, patient_name, dob, gender, mobile, address, membership_id=None):
        pid = self.patient_dao.create_patient(patient_name, dob, gender, mobile, address, membership_id)
        return pid

    def generate_slots_for_doctor(self, doctor_id):
        """
        Returns list of time strings (HH:MM:SS) based on doctor schedule (single row assumed).
        Simple mode — uses first schedule row.
        """
        scheds = self.doctor_dao.get_schedule(doctor_id)
        if not scheds:
            return []
        s = scheds[0]
        # s['StartTime'], s['EndTime'] expected as 'HH:MM:SS' or similar
        start = datetime.strptime(s['StartTime'], "%H:%M:%S").time() if isinstance(s['StartTime'], str) else s['StartTime']
        end = datetime.strptime(s['EndTime'], "%H:%M:%S").time() if isinstance(s['EndTime'], str) else s['EndTime']
        slot_minutes = int(s['SlotDuration']) if s['SlotDuration'] else 20

        slots = []
        cur_dt = datetime.combine(datetime.today(), start)
        end_dt = datetime.combine(datetime.today(), end)
        while cur_dt <= end_dt:
            slots.append(cur_dt.time().strftime("%H:%M:%S"))
            cur_dt += timedelta(minutes=slot_minutes)
        return slots

    # def schedule_appointment(self, patient_id, doctor_id, appointment_date_str, appointment_time_str):
    #     # validate patient & doctor exist
    #     patient = self.patient_dao.get_patient_by_id(patient_id)
    #     if not patient:
    #         raise ValueError("Patient not found.")
    #     doctor = self.doctor_dao.get_doctor_by_id(doctor_id)
    #     if not doctor:
    #         raise ValueError("Doctor not found.")

    #     # check slot availability
    #     if self.appointment_dao.is_slot_taken(appointment_date_str, appointment_time_str, doctor_id):
    #         raise ValueError("Selected slot already taken.")

    #     # get next token
    #     max_token = self.appointment_dao.get_max_token_for_date_doctor(appointment_date_str, doctor_id)
    #     token = max_token + 1

    #     appt_id = self.appointment_dao.create_appointment(appointment_date_str, appointment_time_str, token, patient_id, doctor_id, status='Scheduled')
    #     return appt_id, token
    def schedule_appointment(self, patient_id, doctor_id, appointment_date_str, appointment_time_str):
        # input validation
        try:
            validate_date_str(appointment_date_str)
            validate_time_str(appointment_time_str)
        except ValidationError:
            raise

        # validate patient & doctor exist
        patient = self.patient_dao.get_patient_by_id(patient_id)
        if not patient:
            raise NotFoundError("Patient not found.")
        doctor = self.doctor_dao.get_doctor_by_id(doctor_id)
        if not doctor or int(doctor.get('IsActive', 0)) != 1:
            raise NotFoundError("Doctor not found or inactive.")

        # check slot availability
        if self.appointment_dao.is_slot_taken(appointment_date_str, appointment_time_str, doctor_id):
            raise ConflictError("Selected slot already taken.")

        # get next token
        max_token = self.appointment_dao.get_max_token_for_date_doctor(appointment_date_str, doctor_id)
        token = (max_token or 0) + 1

        appt_id = self.appointment_dao.create_appointment(appointment_date_str, appointment_time_str, token, patient_id, doctor_id, status='Scheduled')
        return appt_id, token

    def view_appointments(self, date_str=None, doctor_id=None):
        # If date_str is None, use today
        if date_str is None:
            date_str = datetime.today().strftime("%Y-%m-%d")
        q = """SELECT a.AppointmentId, a.AppointmentDate, a.AppointmentTime, a.TokenNumber, a.AppointmentStatus,
                      p.PatientName, d.DoctorId
               FROM TblAppointment a
               JOIN TblPatient p ON a.PatientId = p.PatientId
               JOIN TblDoctor d ON a.DoctorId = d.DoctorId
               WHERE a.AppointmentDate = %s"""
        params = [date_str]
        if doctor_id:
            q += " AND a.DoctorId = %s"
            params.append(doctor_id)
        q += " ORDER BY a.AppointmentTime"
        return self.appointment_dao.db.fetch_all(q, tuple(params))

    def generate_billing_for_appointment(self, appointment_id, payment_status='Paid'):
        # compute fees
        consultation_fee = self.billing_dao.compute_consultation_fee(appointment_id)
        lab_charges = self.billing_dao.compute_lab_charges(appointment_id)
        medicine_charges = self.billing_dao.compute_medicine_charges(appointment_id)
        total = consultation_fee + lab_charges + medicine_charges
        bill_id = self.billing_dao.create_billing(appointment_id, consultation_fee, medicine_charges, lab_charges, total, payment_status)
        return {
            'BillingId': bill_id,
            'ConsultationFee': consultation_fee,
            'MedicineCharges': medicine_charges,
            'LabCharges': lab_charges,
            'TotalAmount': total
        }
