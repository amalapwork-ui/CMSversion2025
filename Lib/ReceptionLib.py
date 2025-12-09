# # # Lib/ReceptionLib.py
# # from Dao.PatientDao import PatientDao
# # from Dao.DoctorDao import DoctorDao
# # from Dao.AppointmentDao import AppointmentDao
# # from Dao.BillingDao import BillingDao
# # from datetime import datetime, timedelta, time, date
# # from Utils.SlotUtils import generate_slots_for_schedule, slot_is_on_boundary
# # from Validation.AppointmentValidation import validate_date_str, validate_time_str
# # from Exceptions.Errors import ValidationError, ConflictError, NotFoundError

# # class ReceptionLib:
# #     def __init__(self):
# #         self.patient_dao = PatientDao()
# #         self.doctor_dao = DoctorDao()
# #         self.appointment_dao = AppointmentDao()
# #         self.billing_dao = BillingDao()

# #     # def register_patient(self, patient_name, dob, gender, mobile, address, membership_id=None):
# #     #     pid = self.patient_dao.create_patient(patient_name, dob, gender, mobile, address, membership_id)
# #     #     return pid


# #     def register_patient(self, name, dob, gender, mobile, address):
# #         return self.patient_dao.create_patient(name, dob, gender, mobile, address)


# #     # def generate_slots_for_doctor(self, doctor_id):
# #     #     """
# #     #     Returns list of time strings (HH:MM:SS) based on doctor schedule (single row assumed).
# #     #     Simple mode — uses first schedule row.
# #     #     """
# #     #     scheds = self.doctor_dao.get_schedule(doctor_id)
# #     #     if not scheds:
# #     #         return []
# #     #     s = scheds[0]
# #     #     # s['StartTime'], s['EndTime'] expected as 'HH:MM:SS' or similar
# #     #     start = datetime.strptime(s['StartTime'], "%H:%M:%S").time() if isinstance(s['StartTime'], str) else s['StartTime']
# #     #     end = datetime.strptime(s['EndTime'], "%H:%M:%S").time() if isinstance(s['EndTime'], str) else s['EndTime']
# #     #     slot_minutes = int(s['SlotDuration']) if s['SlotDuration'] else 20

# #     #     slots = []
# #     #     cur_dt = datetime.combine(datetime.today(), start)
# #     #     end_dt = datetime.combine(datetime.today(), end)
# #     #     while cur_dt <= end_dt:
# #     #         slots.append(cur_dt.time().strftime("%H:%M:%S"))
# #     #         cur_dt += timedelta(minutes=slot_minutes)
# #     #     return slots

# #     def generate_slots_for_doctor(self, doctor_id, for_date=None):
# #         """
# #         Returns list of available slots (strings HH:MM:SS) for a given doctor and date.
# #         If for_date supplied (YYYY-MM-DD) we will not filter out already-booked slots here.
# #         The receptionist UI will call this to show possible times.
# #         """
# #         scheds = self.appointment_dao.get_schedule_for_doctor(doctor_id)
# #         if not scheds:
# #             return []

# #         slots = []
# #         for s in scheds:
# #             start = s['StartTime'] if isinstance(s['StartTime'], str) else s['StartTime'].strftime("%H:%M:%S")
# #             end = s['EndTime'] if isinstance(s['EndTime'], str) else s['EndTime'].strftime("%H:%M:%S")
# #             duration = int(s['SlotDuration']) if s.get('SlotDuration') else 15
# #             slots_for_sched = generate_slots_for_schedule(start, end, duration)
# #             slots.extend(slots_for_sched)
# #         # Optionally remove already taken slots if for_date provided
# #         if for_date:
# #             taken = {r['AppointmentTime'] for r in self.appointment_dao.get_appointments_for_doctor_on_date(doctor_id, for_date)}
# #             slots = [t for t in slots if t not in taken]
# #         return slots

# #     # def schedule_appointment(self, patient_id, doctor_id, appointment_date_str, appointment_time_str):
# #     #     # validate patient & doctor exist
# #     #     patient = self.patient_dao.get_patient_by_id(patient_id)
# #     #     if not patient:
# #     #         raise ValueError("Patient not found.")
# #     #     doctor = self.doctor_dao.get_doctor_by_id(doctor_id)
# #     #     if not doctor:
# #     #         raise ValueError("Doctor not found.")

# #     #     # check slot availability
# #     #     if self.appointment_dao.is_slot_taken(appointment_date_str, appointment_time_str, doctor_id):
# #     #         raise ValueError("Selected slot already taken.")

# #     #     # get next token
# #     #     max_token = self.appointment_dao.get_max_token_for_date_doctor(appointment_date_str, doctor_id)
# #     #     token = max_token + 1

# #     #     appt_id = self.appointment_dao.create_appointment(appointment_date_str, appointment_time_str, token, patient_id, doctor_id, status='Scheduled')
# #     #     return appt_id, token
# #     # def schedule_appointment(self, patient_id, doctor_id, appointment_date_str, appointment_time_str):
# #     #     # input validation
# #     #     try:
# #     #         validate_date_str(appointment_date_str)
# #     #         validate_time_str(appointment_time_str)
# #     #     except ValidationError:
# #     #         raise

# #     #     # validate patient & doctor exist
# #     #     patient = self.patient_dao.get_patient_by_id(patient_id)
# #     #     if not patient:
# #     #         raise NotFoundError("Patient not found.")
# #     #     doctor = self.doctor_dao.get_doctor_by_id(doctor_id)
# #     #     if not doctor or int(doctor.get('IsActive', 0)) != 1:
# #     #         raise NotFoundError("Doctor not found or inactive.")

# #     #     # check slot availability
# #     #     if self.appointment_dao.is_slot_taken(appointment_date_str, appointment_time_str, doctor_id):
# #     #         raise ConflictError("Selected slot already taken.")

# #     #     # get next token
# #     #     max_token = self.appointment_dao.get_max_token_for_date_doctor(appointment_date_str, doctor_id)
# #     #     token = (max_token or 0) + 1

# #     #     appt_id = self.appointment_dao.create_appointment(appointment_date_str, appointment_time_str, token, patient_id, doctor_id, status='Scheduled')
# #     #     return appt_id, token

# #     def schedule_appointment(self, patient_id, doctor_id, appointment_date_str, appointment_time_str):
# #             """
# #             Book appointment only if:
# #             - doctor schedule exists
# #             - requested time is exactly a slot boundary
# #             - the slot is not already taken (no overlapping within slot_duration)
# #             """
# #             # validate date & time
# #             try:
# #                 dt = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
# #             except Exception:
# #                 raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

# #             try:
# #                 datetime.strptime(appointment_time_str, "%H:%M:%S")
# #             except Exception:
# #                 raise ValidationError("Invalid time format. Use HH:MM:SS.")

# #             # check patient exists
# #             patient = self.patient_dao.get_patient_by_id(patient_id)
# #             if not patient:
# #                 raise NotFoundError("Patient not found.")

# #             # check doctor and schedule
# #             doctor = self.doctor_dao.get_doctor_by_id(doctor_id)
# #             if not doctor or int(doctor.get('IsActive', 0)) != 1:
# #                 raise NotFoundError("Doctor not found or inactive.")

# #             schedules = self.appointment_dao.get_schedule_for_doctor(doctor_id)
# #             if not schedules:
# #                 raise NotFoundError("No schedule found for this doctor. Add schedule in Admin first.")

# #             # find the schedule row that covers the requested time (some doctors may have multiple schedules)
# #             matched_schedule = None
# #             for s in schedules:
# #                 start = s['StartTime'] if isinstance(s['StartTime'], str) else s['StartTime'].strftime("%H:%M:%S")
# #                 duration = int(s['SlotDuration']) if s.get('SlotDuration') else 15
# #                 # check if requested time is in schedule range and on boundary
# #                 # first, ensure within range (start <= t < end)
# #                 end = s['EndTime'] if isinstance(s['EndTime'], str) else s['EndTime'].strftime("%H:%M:%S")
# #                 fmt = "%H:%M:%S"
# #                 start_dt = datetime.strptime(start, fmt)
# #                 end_dt = datetime.strptime(end, fmt)
# #                 req_dt = datetime.strptime(appointment_time_str, fmt)
# #                 if start_dt <= req_dt < end_dt and slot_is_on_boundary(appointment_time_str, start, duration):
# #                     matched_schedule = s
# #                     break

# #             if not matched_schedule:
# #                 # build friendly message with available slots for that doctor
# #                 possible_slots = self.generate_slots_for_doctor(doctor_id, for_date=appointment_date_str)
# #                 raise ValidationError(f"Requested time is not a valid slot for this doctor. Available slots example: {possible_slots[:8]}")

# #             # now check overlapping appointments using schedule duration
# #             slot_minutes = int(matched_schedule.get('SlotDuration') or 15)
# #             if self.appointment_dao.is_slot_taken_exact(doctor_id, appointment_date_str, appointment_time_str, slot_minutes):
# #                 # suggest next available slot (simple linear search)
# #                 # build all slots and find the first not-taken that is after requested time
# #                 all_slots = generate_slots_for_schedule(matched_schedule['StartTime'].strftime("%H:%M:%S") if not isinstance(matched_schedule['StartTime'], str) else matched_schedule['StartTime'],
# #                                                         matched_schedule['EndTime'].strftime("%H:%M:%S") if not isinstance(matched_schedule['EndTime'], str) else matched_schedule['EndTime'],
# #                                                         slot_minutes)
# #                 taken = {r['AppointmentTime'] for r in self.appointment_dao.get_appointments_for_doctor_on_date(doctor_id, appointment_date_str)}
# #                 for s in all_slots:
# #                     # pick first slot after requested_time that is not taken
# #                     if s > appointment_time_str and s not in taken:
# #                         return None, f"Requested slot is taken. Next available slot: {s}"
# #                 raise ConflictError("Requested slot is already taken and no later slots are available for that schedule on the selected date.")

# #             # compute token
# #             max_token = self.appointment_dao.get_max_token_for_date_doctor(appointment_date_str, doctor_id) or 0
# #             token = max_token + 1

# #             # all clear — create appointment
# #             appt_id = self.appointment_dao.create_appointment(appointment_date_str, appointment_time_str, token, patient_id, doctor_id, status='Scheduled')
# #             return appt_id, token

# #     def view_appointments(self, date_str=None, doctor_id=None):
# #         # If date_str is None, use today
# #         if date_str is None:
# #             date_str = datetime.today().strftime("%Y-%m-%d")
# #         q = """SELECT a.AppointmentId, a.AppointmentDate, a.AppointmentTime, a.TokenNumber, a.AppointmentStatus,
# #                       p.PatientName, d.DoctorId
# #                FROM TblAppointment a
# #                JOIN TblPatient p ON a.PatientId = p.PatientId
# #                JOIN TblDoctor d ON a.DoctorId = d.DoctorId
# #                WHERE a.AppointmentDate = %s"""
# #         params = [date_str]
# #         if doctor_id:
# #             q += " AND a.DoctorId = %s"
# #             params.append(doctor_id)
# #         q += " ORDER BY a.AppointmentTime"
# #         return self.appointment_dao.db.fetch_all(q, tuple(params))

# #     def generate_billing_for_appointment(self, appointment_id, payment_status='Paid'):
# #         # compute fees
# #         consultation_fee = self.billing_dao.compute_consultation_fee(appointment_id)
# #         lab_charges = self.billing_dao.compute_lab_charges(appointment_id)
# #         medicine_charges = self.billing_dao.compute_medicine_charges(appointment_id)
# #         total = consultation_fee + lab_charges + medicine_charges
# #         bill_id = self.billing_dao.create_billing(appointment_id, consultation_fee, medicine_charges, lab_charges, total, payment_status)
# #         return {
# #             'BillingId': bill_id,
# #             'ConsultationFee': consultation_fee,
# #             'MedicineCharges': medicine_charges,
# #             'LabCharges': lab_charges,
# #             'TotalAmount': total
# #         }
# #     def generate_slots(self, start_time, end_time, duration):
# #         from datetime import datetime, timedelta

# #         fmt = "%H:%M:%S"
# #         start = datetime.strptime(str(start_time), fmt)
# #         end = datetime.strptime(str(end_time), fmt)

# #         slots = []
# #         while start < end:
# #             slots.append(start.strftime("%H:%M:%S"))
# #             start += timedelta(minutes=duration)

# #         return slots


# # Lib/ReceptionLib.py
# from Dao.PatientDao import PatientDao
# from Dao.DoctorDao import DoctorDao
# from Dao.AppointmentDao import AppointmentDao
# from Dao.BillingDao import BillingDao
# from Exceptions.Errors import ValidationError, NotFoundError, ConflictError
# from Utils.SlotUtils import generate_slots_for_schedule, slot_is_on_boundary
# from datetime import datetime

# class ReceptionLib:
#     def __init__(self):
#         self.patient_dao = PatientDao()
#         self.doctor_dao = DoctorDao()
#         self.appointment_dao = AppointmentDao()
#         self.billing_dao = BillingDao()

#     def generate_slots_for_doctor(self, doctor_id, for_date=None):
#         """
#         Returns list of available slots (strings HH:MM:SS) for a doctor.
#         If for_date provided (YYYY-MM-DD), taken slots are filtered out.
#         """
#         schedules = self.doctor_dao.get_schedules_for_doctor(doctor_id)
#         if not schedules:
#             return []
#         all_slots = []
#         for s in schedules:
#             start = s['StartTime'] if isinstance(s['StartTime'], str) else s['StartTime'].strftime("%H:%M:%S")
#             end = s['EndTime'] if isinstance(s['EndTime'], str) else s['EndTime'].strftime("%H:%M:%S")
#             duration = int(s['SlotDuration']) if s.get('SlotDuration') else 15
#             slots = generate_slots_for_schedule(start, end, duration)
#             all_slots.extend(slots)
#         if for_date:
#             taken = {r['AppointmentTime'] for r in self.appointment_dao.get_appointments_for_doctor_on_date(doctor_id, for_date)}
#             all_slots = [t for t in all_slots if t not in taken]
#         # dedupe & sort
#         return sorted(list(dict.fromkeys(all_slots)))

#     def schedule_appointment(self, patient_id, doctor_id, appointment_date_str, appointment_time_str):
#         # validate formats
#         try:
#             date_obj = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
#         except Exception:
#             raise ValidationError("Invalid date format (YYYY-MM-DD).")
#         try:
#             datetime.strptime(appointment_time_str, "%H:%M:%S")
#         except Exception:
#             raise ValidationError("Invalid time format (HH:MM:SS).")

#         # check patient & doctor exist
#         patient = self.patient_dao.get_patient_by_id(patient_id)
#         if not patient:
#             raise NotFoundError("Patient not found.")
#         doctor = self.doctor_dao.get_doctor_by_id(doctor_id)
#         if not doctor or int(doctor.get('IsActive', 0)) != 1:
#             raise NotFoundError("Doctor not found or inactive.")

#         schedules = self.doctor_dao.get_schedules_for_doctor(doctor_id)
#         if not schedules:
#             raise NotFoundError("No schedule found for this doctor. Ask doctor to create one.")

#         # find the schedule that covers requested time and validate boundary
#         matched = None
#         for s in schedules:
#             start = s['StartTime'] if isinstance(s['StartTime'], str) else s['StartTime'].strftime("%H:%M:%S")
#             end = s['EndTime'] if isinstance(s['EndTime'], str) else s['EndTime'].strftime("%H:%M:%S")
#             duration = int(s['SlotDuration']) if s.get('SlotDuration') else 15
#             fmt = "%H:%M:%S"
#             start_dt = datetime.strptime(start, fmt)
#             end_dt = datetime.strptime(end, fmt)
#             req_dt = datetime.strptime(appointment_time_str, fmt)
#             if start_dt <= req_dt < end_dt and slot_is_on_boundary(appointment_time_str, start, duration):
#                 matched = s
#                 break

#         if not matched:
#             avail = self.generate_slots_for_doctor(doctor_id, for_date=appointment_date_str)
#             raise ValidationError(f"Requested time not valid. Example available slots: {avail[:8]}")

#         slot_minutes = int(matched.get('SlotDuration') or 15)
#         # check overlapping
#         if self.appointment_dao.is_slot_taken_exact(doctor_id, appointment_date_str, appointment_time_str, slot_minutes):
#             # find next free slot after requested
#             all_slots = generate_slots_for_schedule(matched['StartTime'] if isinstance(matched['StartTime'], str) else matched['StartTime'].strftime("%H:%M:%S"),
#                                                     matched['EndTime'] if isinstance(matched['EndTime'], str) else matched['EndTime'].strftime("%H:%M:%S"),
#                                                     slot_minutes)
#             taken = {r['AppointmentTime'] for r in self.appointment_dao.get_appointments_for_doctor_on_date(doctor_id, appointment_date_str)}
#             for s in all_slots:
#                 if s > appointment_time_str and s not in taken:
#                     return None, f"Requested slot taken. Next available: {s}"
#             raise ConflictError("Requested slot is taken and no later slots available for that schedule on the selected date.")

#         # token
#         max_token = self.appointment_dao.get_max_token_for_date_doctor(appointment_date_str, doctor_id) or 0
#         token = max_token + 1
#         appt_id = self.appointment_dao.create_appointment(appointment_date_str, appointment_time_str, token, patient_id, doctor_id)
#         return appt_id, token


from Dao.PatientDao import PatientDao
from Dao.DoctorDao import DoctorDao
from Dao.AppointmentDao import AppointmentDao
from Dao.BillingDao import BillingDao
from Exceptions.Errors import ValidationError, NotFoundError, ConflictError
from Utils.SlotUtils import generate_slots_for_schedule, slot_is_on_boundary
from datetime import datetime

class ReceptionLib:
    def __init__(self):
        self.patient_dao = PatientDao()
        self.doctor_dao = DoctorDao()
        self.appointment_dao = AppointmentDao()
        self.billing_dao = BillingDao()

    def register_patient(self, name, dob, gender, mobile, address):
        return self.patient_dao.create_patient(name, dob, gender, mobile, address)

    def generate_slots_for_doctor(self, doctor_id, for_date=None):
        """Generates all possible slots based on doctor's schedule"""
        schedules = self.doctor_dao.get_schedules_for_doctor(doctor_id)
        if not schedules:
            return []
        
        all_slots = []
        for s in schedules:
            # Handle potential time objects or strings from DB
            start = str(s['StartTime'])
            end = str(s['EndTime'])
            duration = int(s['SlotDuration'])
            
            slots = generate_slots_for_schedule(start, end, duration)
            all_slots.extend(slots)

        # Filter out taken slots if date is provided
        if for_date:
            taken_appts = self.appointment_dao.get_appointments_for_doctor_on_date(doctor_id, for_date)
            # Create a set of taken times for O(1) lookup
            taken_times = {str(a['AppointmentTime']) for a in taken_appts}
            all_slots = [t for t in all_slots if t not in taken_times]
            
        return sorted(list(set(all_slots))) # Unique and sorted

    def schedule_appointment(self, patient_id, doctor_id, date_str, time_str):
        # 1. Existence Checks
        if not self.patient_dao.get_patient_by_id(patient_id):
            raise NotFoundError("Patient ID not found.")
        
        doc = self.doctor_dao.get_doctor_by_id(doctor_id)
        if not doc or not doc['IsActive']:
            raise NotFoundError("Doctor not found or inactive.")

        # 2. Schedule Boundary Check
        schedules = self.doctor_dao.get_schedules_for_doctor(doctor_id)
        valid_slot = False
        slot_duration = 15 # Default fallback

        fmt = "%H:%M:%S"
        try:
            req_time = datetime.strptime(time_str, fmt)
        except ValueError:
             # handle case where time_str might be a timedelta or other format
             req_time = datetime.strptime(str(time_str), fmt)

        for s in schedules:
            start = datetime.strptime(str(s['StartTime']), fmt)
            end = datetime.strptime(str(s['EndTime']), fmt)
            dur = int(s['SlotDuration'])
            
            if start <= req_time < end:
                if slot_is_on_boundary(time_str, str(s['StartTime']), dur):
                    valid_slot = True
                    slot_duration = dur
                    break
        
        if not valid_slot:
            raise ValidationError("Time is not a valid slot in doctor's schedule.")

        # 3. Conflict Check (Double Booking)
        if self.appointment_dao.is_slot_taken_exact(doctor_id, date_str, time_str, slot_duration):
            raise ConflictError("Slot already taken.")

        # 4. Create
        token = self.appointment_dao.get_max_token_for_date_doctor(date_str, doctor_id) + 1
        appt_id = self.appointment_dao.create_appointment(date_str, time_str, token, patient_id, doctor_id)
        return appt_id, token

    def view_appointments(self, date_str=None, doctor_id=None):
        if not date_str:
            date_str = datetime.today().strftime("%Y-%m-%d")
        
        if doctor_id:
            return self.appointment_dao.get_appointments_for_doctor_on_date(doctor_id, date_str)
        else:
            return []

    def generate_bill(self, appt_id):
        # Recalculate totals
        cons_fee = self.billing_dao.compute_consultation_fee(appt_id)
        lab_fee = self.billing_dao.compute_lab_charges(appt_id)
        med_fee = self.billing_dao.compute_medicine_charges(appt_id)
        total = cons_fee + lab_fee + med_fee
        
        bill_id = self.billing_dao.create_billing(appt_id, cons_fee, med_fee, lab_fee, total)
        return bill_id, total