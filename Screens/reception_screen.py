# # Screens/reception_screen.py
# from Lib.ReceptionLib import ReceptionLib


# class ReceptionScreen:
#     def __init__(self):
#         self.lib = ReceptionLib()

#     def menu(self):
#         while True:
#             print("\n=== RECEPTIONIST DASHBOARD ===")
#             print("1. Register New Patient")
#             print("2. Schedule Appointment")
#             print("3. View Appointments")
#             print("4. Generate Billing")
#             print("5. Logout")

#             ch = input("Choice: ").strip()
#             try:
#                 if ch == '1':
#                     name = input("Patient Name: ").strip()
#                     dob = input("DOB (YYYY-MM-DD): ").strip()
#                     gender = input("Gender (M/F/O): ").strip()
#                     mobile = input("Mobile Number: ").strip()
#                     address = input("Address: ").strip()
#                     pid = self.lib.register_patient(name, dob, gender, mobile, address)
#                     print(f"Patient created. PatientId: {pid}")
#                 elif ch == '2':
#                     patient_id = input("Patient ID: ").strip()
#                     doctor_id = input("Doctor ID: ").strip()
#                     date = input("Appointment Date (YYYY-MM-DD): ").strip()
#                     # show available slots
#                     slots = self.lib.generate_slots_for_doctor(int(doctor_id))
#                     if not slots:
#                         print("No schedule found for doctor.")
#                         continue
#                     print("Available slots (sample) — please choose a time from these:")
#                     for s in slots[:20]:
#                         print(s)
#                     time_slot = input("Choose time (HH:MM:SS): ").strip()
#                     appt_id, token = self.lib.schedule_appointment(int(patient_id), int(doctor_id), date, time_slot)
#                     print(f"Appointment booked. ID: {appt_id}, Token: {token}")
#                 elif ch == '3':
#                     date = input("Date (YYYY-MM-DD) [enter for today]: ").strip() or None
#                     doctor_id = input("Doctor ID (optional): ").strip() or None
#                     appts = self.lib.view_appointments(date, int(doctor_id) if doctor_id else None)
#                     if not appts:
#                         print("No appointments found.")
#                     else:
#                         for a in appts:
#                             print(f"ApptID:{a['AppointmentId']} Date:{a['AppointmentDate']} Time:{a['AppointmentTime']} Token:{a['TokenNumber']} Patient:{a['PatientName']} Status:{a['AppointmentStatus']}")
#                 elif ch == '4':
#                     appt_id = input("Appointment ID: ").strip()
#                     bill = self.lib.generate_billing_for_appointment(int(appt_id))
#                     print("Bill generated:")
#                     print(bill)
#                 elif ch == '5':
#                     print("Logging out...")
#                     break
#                 else:
#                     print("Invalid choice.")
#             except Exception as e:
#                 print("Error:", str(e))


# Screens/reception_screen.py  (replace menu method)
from Lib.ReceptionLib import ReceptionLib
from Utils.InputUtils import input_str, input_date, input_time, input_int, confirm
from Validation.PatientValidation import validate_mobile, validate_patient_name
from Exceptions.Errors import ValidationError

class ReceptionScreen:
    def __init__(self):
        self.lib = ReceptionLib()

    def menu(self):
        while True:
            print("\n=== RECEPTIONIST DASHBOARD ===")
            print("1. Register New Patient")
            print("2. Schedule Appointment")
            print("3. View Appointments")
            print("4. Generate Billing")
            print("5. Logout")

            ch = input_str("Choice: ", required=True)
            try:
                if ch == '1':
                    name = input_str("Patient Name: ")
                    validate_patient_name(name)
                    dob = input_date("DOB (YYYY-MM-DD): ")
                    gender = input_str("Gender (M/F/O): ")
                    mobile = input_str("Mobile Number: ")
                    validate_mobile(mobile)
                    address = input_str("Address: ", required=False)
                    pid = self.lib.register_patient(name, dob, gender, mobile, address)
                    print(f"Patient created. PatientId: {pid}")

                elif ch == '2':
                    patient_id = input_int("Patient ID: ")
                    doctor_id = input_int("Doctor ID: ")
                    date = input_date("Appointment Date (YYYY-MM-DD): ")
                    slots = self.lib.generate_slots_for_doctor(int(doctor_id))
                    if not slots:
                        print("No schedule found for doctor.")
                        continue
                    print("Available slots (first 20):")
                    for s in slots[:20]:
                        print(s)
                    time_slot = input_time("Choose time (HH:MM:SS): ")
                    # validate format
                    appt_id, token = self.lib.schedule_appointment(int(patient_id), int(doctor_id), date, time_slot)
                    print(f"Appointment booked. ID: {appt_id}, Token: {token}")

                elif ch == '3':
                    date = input_str("Date (YYYY-MM-DD) [enter for today]: ", required=False)
                    doctor_id = input_str("Doctor ID (optional): ", required=False)
                    appts = self.lib.view_appointments(date or None, int(doctor_id) if doctor_id else None)
                    if not appts:
                        print("No appointments found.")
                    else:
                        for a in appts:
                            print(f"ApptID:{a['AppointmentId']} Date:{a['AppointmentDate']} Time:{a['AppointmentTime']} Token:{a['TokenNumber']} Patient:{a['PatientName']} Status:{a['AppointmentStatus']}")

                elif ch == '4':
                    appt_id = input_int("Appointment ID: ")
                    bill = self.lib.generate_billing_for_appointment(int(appt_id))
                    print("Bill generated:")
                    print(bill)

                elif ch == '5':
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice.")
            except ValidationError as ve:
                print("Validation error:", ve)
            except Exception as e:
                # catch-all with friendly message
                print("Operation failed:", e)
