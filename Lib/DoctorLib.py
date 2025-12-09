# # Lib/DoctorLib.py
# from Dao.DoctorDao import DoctorDao
# from Dao.AppointmentDao import AppointmentDao
# from Dao.ConsultationDao import ConsultationDao
# from Dao.PrescriptionDao import PrescriptionDao
# from Dao.LabTestPrescriptionDao import LabTestPrescriptionDao

# from Validation.ConsultationValidation import validate_symptoms, validate_diagnosis
# from Exceptions.Errors import NotFoundError, PermissionError, ValidationError

# class DoctorLib:
#     def __init__(self, doctor_id):
#         self.doctor_id = doctor_id
#         self.doctor_dao = DoctorDao()
#         self.app_dao = AppointmentDao()
#         self.consult_dao = ConsultationDao()
#         self.presc_dao = PrescriptionDao()
#         self.lab_presc_dao = LabTestPrescriptionDao()

#     def view_todays_appointments(self):
#         appts = self.app_dao.get_todays_appointments_for_doctor(self.doctor_id)
#         return appts

#     # def start_consultation(self, appointment_id):
#     #     # ensure appointment belongs to doctor and is scheduled/checked-in
#     #     appt = self.app_dao.get_appointment_by_id(appointment_id)
#     #     if not appt:
#     #         raise ValueError("Appointment not found.")
#     #     if int(appt['DoctorId']) != int(self.doctor_id):
#     #         raise PermissionError("This appointment is not assigned to you.")
#     #     # Insert consultation
#     #     symptoms = input("Enter Symptoms: ").strip()
#     #     diagnosis = input("Enter Diagnosis: ").strip()
#     #     notes = input("Enter Notes (optional): ").strip()
#     #     consult_id = self.consult_dao.insert_consultation(appointment_id, symptoms, diagnosis, notes)
#     #     # Update appointment status to Completed
#     #     self.app_dao.update_status(appointment_id, 'Completed')
#     #     return consult_id
#     def start_consultation(self, appointment_id):
#         appt = self.app_dao.get_appointment_by_id(appointment_id)
#         if not appt:
#             raise NotFoundError("Appointment not found.")
#         if int(appt['DoctorId']) != int(self.doctor_id):
#             raise PermissionError("This appointment is not assigned to you.")
#         if appt.get('AppointmentStatus') not in ('Scheduled','Checked-In'):
#             # allow starting only if scheduled or checked-in
#             raise ValidationError("Appointment status must be 'Scheduled' or 'Checked-In' to start consultation.")

#         symptoms = input("Enter Symptoms: ").strip()
#         validate_symptoms(symptoms)
#         diagnosis = input("Enter Diagnosis: ").strip()
#         validate_diagnosis(diagnosis)
#         notes = input("Enter Notes (optional): ").strip()

#         consult_id = self.consult_dao.insert_consultation(appointment_id, symptoms, diagnosis, notes)
#         # Update appointment status to Completed
#         self.app_dao.update_status(appointment_id, 'Completed')
#         return consult_id

#     def prescribe_medicine(self, appointment_id):
#         # add multiple meds
#         while True:
#             med_id = input("Enter MedicineId (or 'q' to quit): ").strip()
#             if med_id.lower() == 'q':
#                 break
#             dosage = input("Dosage (e.g. '1 tablet'): ").strip()
#             frequency = input("Frequency (e.g. '1-0-1'): ").strip()
#             duration = input("Duration (e.g. '3 days'): ").strip()
#             self.presc_dao.insert_medicine_prescription(med_id, dosage, frequency, duration, appointment_id)
#             print("Medicine added.")
#         return True

#     def prescribe_lab_test(self, appointment_id):
#         while True:
#             lab_id = input("Enter LabTestId (or 'q' to quit): ").strip()
#             if lab_id.lower() == 'q':
#                 break
#             notes = input("Add notes (optional): ").strip()
#             self.lab_presc_dao.insert_labtest_prescription(lab_id, notes, appointment_id)
#             print("Lab test request added.")
#         return True

#     def view_patient_history(self, patient_id):
#         consultations = self.consult_dao.get_consultations_by_patient(patient_id)
#         prescriptions = []  # you can call PrescriptionDao methods to fetch old prescriptions if implemented
#         labtests = []  # similarly for labtest history when necessary
#         return {
#             'consultations': consultations,
#             'prescriptions': prescriptions,
#             'labtests': labtests
#         }
    
#     # schedule management (doctor actions)
#     def view_my_schedules(self):
#         return self.doctor_dao.get_schedules_for_doctor(self.doctor_id)

#     def add_schedule(self, start_time, end_time, slot_duration):
#         # basic validation
#         from Utils.SlotUtils import generate_slots_for_schedule
#         slots = generate_slots_for_schedule(start_time, end_time, int(slot_duration))
#         if not slots:
#             raise ValidationError("Start time must be before end time and result in at least one slot.")
#         return self.doctor_dao.add_schedule(self.doctor_id, start_time, end_time, slot_duration)

#     def update_schedule(self, schedule_id, start_time, end_time, slot_duration, is_active=1):
#         return self.doctor_dao.update_schedule(schedule_id, start_time, end_time, slot_duration, is_active)

#     def remove_schedule(self, schedule_id):
#         return self.doctor_dao.delete_schedule(schedule_id)

# # Lib/DoctorLib.py
from datetime import datetime
from Dao.DoctorDao import DoctorDao
from Dao.AppointmentDao import AppointmentDao
from Dao.ConsultationDao import ConsultationDao
from Dao.PrescriptionDao import PrescriptionDao
from Dao.LabTestPrescriptionDao import LabTestPrescriptionDao
from Validation.ConsultationValidation import validate_symptoms, validate_diagnosis
from Exceptions.Errors import NotFoundError, PermissionError, ValidationError

class DoctorLib:
    def __init__(self, doctor_id):
        self.doctor_id = doctor_id
        self.doctor_dao = DoctorDao()
        self.app_dao = AppointmentDao()
        self.consult_dao = ConsultationDao()
        self.presc_dao = PrescriptionDao()
        self.lab_presc_dao = LabTestPrescriptionDao()

    def view_todays_appointments(self):
        today_str = datetime.today().strftime('%Y-%m-%d')
        return self.app_dao.get_appointments_for_doctor_on_date(self.doctor_id, today_str)

    def start_consultation(self, appointment_id, symptoms, diagnosis, notes):
        # 1. Validate Ownership
        appt = self.app_dao.get_appointment_by_id(appointment_id)
        if not appt:
            raise NotFoundError("Appointment not found.")
        
        # Convert IDs to int for safe comparison
        if int(appt['DoctorId']) != int(self.doctor_id):
            raise PermissionError("This appointment is not assigned to you.")
        
        # 2. Validate Status (Optional: restrict to Scheduled/Checked-In)
        if appt['AppointmentStatus'] == 'Completed':
             raise ValidationError("This appointment is already completed.")

        # 3. Validate Data
        validate_symptoms(symptoms)
        validate_diagnosis(diagnosis)

        # 4. Perform Action
        consult_id = self.consult_dao.insert_consultation(appointment_id, symptoms, diagnosis, notes)
        self.app_dao.update_status(appointment_id, 'Completed')
        return consult_id

    def prescribe_medicine(self, appointment_id, medicine_id, dosage, frequency, duration):
        # In a real app, validate medicine_id exists here using MedicineDao
        return self.presc_dao.insert_medicine_prescription(medicine_id, dosage, frequency, duration, appointment_id)

    def prescribe_lab_test(self, appointment_id, lab_test_id, notes):
        # Validate lab_test_id exists here
        return self.lab_presc_dao.insert_labtest_prescription(lab_test_id, notes, appointment_id)

    def view_patient_history(self, patient_id):
        return self.consult_dao.get_consultations_by_patient(patient_id)

    # --- Schedule Management ---
    def view_my_schedules(self):
        return self.doctor_dao.get_schedules_for_doctor(self.doctor_id)

    def add_schedule(self, start, end, slot):
        # Logic to ensure start < end handled in Screen or Utils
        return self.doctor_dao.add_schedule(self.doctor_id, start, end, slot)

    def update_schedule(self, schedule_id, start, end, slot, is_active):
        return self.doctor_dao.update_schedule(schedule_id, start, end, slot, is_active)

    def remove_schedule(self, schedule_id):
        return self.doctor_dao.delete_schedule(schedule_id)