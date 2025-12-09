# # # Screens/doctor_screen.py
# # from Lib.DoctorLib import DoctorLib
# # from Exceptions.Errors import ValidationError, NotFoundError

# # class DoctorScreen:
# #     def __init__(self, doctor_id):
# #         self.lib = DoctorLib(doctor_id)
# #         self.doctor_id = doctor_id

# #     def menu(self):
# #         while True:
# #             print("\n=== DOCTOR DASHBOARD ===")
# #             print("1. View Today's Appointments")
# #             print("2. Start Consultation")
# #             print("3. Prescribe Medicines")
# #             print("4. Prescribe Lab Tests")
# #             print("5. View Patient History")
# #             print("6. Logout")

# #             ch = input("Choice: ").strip()
# #             try:
# #                 if ch == '1':
# #                     appts = self.lib.view_todays_appointments()
# #                     if not appts:
# #                         print("No appointments for today.")
# #                     else:
# #                         for a in appts:
# #                             print(f"ApptID: {a['AppointmentId']} | Token: {a['TokenNumber']} | Time: {a['AppointmentTime']} | Patient: {a['PatientName']} | Status: {a['AppointmentStatus']}")
# #                 elif ch == '2':
# #                     appt_id = input("Enter Appointment ID: ").strip()
# #                     cid = self.lib.start_consultation(appt_id)
# #                     print("Consultation recorded. ID:", cid)
# #                 elif ch == '3':
# #                     appt_id = input("Enter Appointment ID: ").strip()
# #                     self.lib.prescribe_medicine(appt_id)
# #                     print("Medicine prescription saved.")
# #                 elif ch == '4':
# #                     appt_id = input("Enter Appointment ID: ").strip()
# #                     self.lib.prescribe_lab_test(appt_id)
# #                     print("Lab tests requested.")
# #                 elif ch == '5':
# #                     patient_id = input("Enter Patient ID: ").strip()
# #                     hist = self.lib.view_patient_history(patient_id)
# #                     print("Consultations:")
# #                     for c in hist['consultations']:
# #                         print(f"- {c['CreatedDate']} | {c['Symptoms']} | {c['Diagnosis']}")
# #                 elif ch == '6':
# #                     print("Logging out...")
# #                     break
# #                 else:
# #                     print("Invalid choice.")
# #             except Exception as e:
# #                 print("Error:", str(e))
# #             # Screens/doctor_screen.py  (inside menu try/except blocks)
# #             except ValidationError as ve:
# #                 print("Invalid input:", ve)
# #             except PermissionError as pe:
# #                 print("Permission error:", pe)
# #             except NotFoundError as nf:
# #                 print("Not found:", nf)
# #             except Exception as e:
# #                 print("Operation failed:", e)

# # Screens/doctor_screen.py
# from Lib.DoctorLib import DoctorLib
# from Utils.InputUtils import input_str, input_time, input_int
# from Exceptions.Errors import ValidationError
# from datetime import datetime

# class DoctorScreen:
#     def __init__(self, doctor_id):
#         self.lib = DoctorLib(doctor_id)
#         self.doctor_id = doctor_id

#     def menu(self):
#         while True:
#             print("\n=== DOCTOR DASHBOARD ===")
#             print("1. View Today's Appointments")
#             print("2. Start Consultation")
#             print("3. Prescribe Medicines")
#             print("4. Prescribe Lab Tests")
#             print("5. View Patient History")
#             print("6. Manage My Schedule")
#             print("7. Logout")
#             ch = input_str("Choice: ")
#             try:
#                 if ch == '1':
#                     # existing logic depends on AppointmentDao.get_todays_appointments_for_doctor
#                     from Dao.AppointmentDao import AppointmentDao
#                     ad = AppointmentDao()
#                     appts = ad.get_appointments_for_doctor_on_date(self.doctor_id, datetime.today().strftime("%Y-%m-%d"))
#                     if not appts:
#                         print("No appointments for today.")
#                     else:
#                         for a in appts:
#                             print(f"ApptID: {a['AppointmentId']} | Time: {a['AppointmentTime']} | PatientId: {a['PatientId']} | Token: {a['TokenNumber']} | Status: {a['AppointmentStatus']}")
#                 elif ch == '6':
#                     self.manage_schedule_menu()
#                 elif ch == '7':
#                     print("Logging out...")
#                     break
#                 else:
#                     print("Not implemented in this snippet (use earlier Doctor actions).")
#             except ValidationError as ve:
#                 print("Validation:", ve)
#             except Exception as e:
#                 print("Error:", e)

#     def manage_schedule_menu(self):
#         while True:
#             print("\n--- Manage My Schedule ---")
#             print("1. View My Schedules")
#             print("2. Add Schedule")
#             print("3. Update Schedule")
#             print("4. Remove (Deactivate) Schedule")
#             print("5. Back")
#             ch = input_str("Choice: ")
#             try:
#                 if ch == '1':
#                     rows = self.lib.view_my_schedules()
#                     if not rows:
#                         print("No schedules found.")
#                     else:
#                         for r in rows:
#                             print(r)
#                 elif ch == '2':
#                     start = input_time("Start time (HH:MM:SS): ")
#                     end = input_time("End time (HH:MM:SS): ")
#                     slot = input_int("Slot duration (minutes): ")
#                     sid = self.lib.add_schedule(start, end, slot)
#                     print("Schedule added ID:", sid)
#                 elif ch == '3':
#                     sid = input_int("Schedule ID to update: ")
#                     start = input_time("Start time (HH:MM:SS): ")
#                     end = input_time("End time (HH:MM:SS): ")
#                     slot = input_int("Slot duration (minutes): ")
#                     act = input_int("IsActive (1/0): ")
#                     self.lib.update_schedule(sid, start, end, slot, act)
#                     print("Updated.")
#                 elif ch == '4':
#                     sid = input_int("Schedule ID to remove (deactivate): ")
#                     self.lib.remove_schedule(sid)
#                     print("Deactivated.")
#                 elif ch == '5':
#                     break
#             except ValidationError as ve:
#                 print("Validation:", ve)
#             except Exception as e:
#                 print("Error:", e)


from Lib.DoctorLib import DoctorLib
from Utils.InputUtils import input_str, input_int, input_time, confirm
from Exceptions.Errors import ValidationError, NotFoundError, PermissionError

class DoctorScreen:
    def __init__(self, doctor_id):
        self.lib = DoctorLib(doctor_id)

    def menu(self):
        while True:
            print("\n=== DOCTOR DASHBOARD ===")
            print("1. View Today's Appointments")
            print("2. Start Consultation")
            print("3. Prescribe Medicines")
            print("4. Prescribe Lab Tests")
            print("5. Patient History")
            print("6. Manage Schedule")
            print("7. Logout")

            ch = input_str("Choice: ")

            try:
                if ch == '1':
                    appts = self.lib.view_todays_appointments()
                    if not appts:
                        print("No appointments found.")
                    else:
                        print(f"{'ApptID':<8} {'Time':<10} {'Patient':<20} {'Status'}")
                        print("-" * 50)
                        for a in appts:
                            print(f"{a['AppointmentId']:<8} {a['AppointmentTime']} {a['PatientName']:<20} {a['AppointmentStatus']}")

                elif ch == '2':
                    appt_id = input_int("Enter Appointment ID: ")
                    sym = input_str("Symptoms: ")
                    diag = input_str("Diagnosis: ")
                    note = input_str("Notes (optional): ", required=False)
                    
                    cid = self.lib.start_consultation(appt_id, sym, diag, note)
                    print(f"✅ Consultation saved! ID: {cid}")

                elif ch == '3':
                    appt_id = input_int("Enter Appointment ID: ")
                    while True:
                        med_id = input_int("Medicine ID: ")
                        dose = input_str("Dosage (e.g. 1-0-1): ")
                        freq = input_str("Frequency (e.g. Daily): ")
                        dur = input_str("Duration (e.g. 5 days): ")
                        
                        self.lib.prescribe_medicine(appt_id, med_id, dose, freq, dur)
                        print("Medicine added.")
                        
                        if not confirm("Add another medicine? (y/n): "):
                            break

                elif ch == '4':
                    appt_id = input_int("Enter Appointment ID: ")
                    while True:
                        lab_id = input_int("Lab Test ID: ")
                        notes = input_str("Lab Notes: ", required=False)
                        self.lib.prescribe_lab_test(appt_id, lab_id, notes)
                        print("Lab test prescribed.")
                        if not confirm("Add another test? (y/n): "):
                            break

                elif ch == '5':
                    pid = input_int("Enter Patient ID: ")
                    history = self.lib.view_patient_history(pid)
                    print("\n--- History ---")
                    for h in history:
                        print(f"Date: {h['CreatedDate']} | Dx: {h['Diagnosis']}")

                elif ch == '6':
                    self.schedule_menu()

                elif ch == '7':
                    break
            except (ValidationError, NotFoundError, PermissionError) as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ System Error: {e}")

    def schedule_menu(self):
        print("\n--- My Schedule ---")
        rows = self.lib.view_my_schedules()
        for r in rows:
            print(f"ID: {r['ScheduleId']} | {r['StartTime']} - {r['EndTime']} | {r['SlotDuration']} mins")
        
        if confirm("Add new schedule? (y/n): "):
            start = input_time("Start Time (HH:MM:SS): ")
            end = input_time("End Time (HH:MM:SS): ")
            slot = input_int("Slot Duration (mins): ")
            self.lib.add_schedule(start, end, slot)
            print("Schedule added.")