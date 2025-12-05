# Screens/doctor_screen.py
from Lib.DoctorLib import DoctorLib
from Exceptions.Errors import ValidationError, NotFoundError

class DoctorScreen:
    def __init__(self, doctor_id):
        self.lib = DoctorLib(doctor_id)
        self.doctor_id = doctor_id

    def menu(self):
        while True:
            print("\n=== DOCTOR DASHBOARD ===")
            print("1. View Today's Appointments")
            print("2. Start Consultation")
            print("3. Prescribe Medicines")
            print("4. Prescribe Lab Tests")
            print("5. View Patient History")
            print("6. Logout")

            ch = input("Choice: ").strip()
            try:
                if ch == '1':
                    appts = self.lib.view_todays_appointments()
                    if not appts:
                        print("No appointments for today.")
                    else:
                        for a in appts:
                            print(f"ApptID: {a['AppointmentId']} | Token: {a['TokenNumber']} | Time: {a['AppointmentTime']} | Patient: {a['PatientName']} | Status: {a['AppointmentStatus']}")
                elif ch == '2':
                    appt_id = input("Enter Appointment ID: ").strip()
                    cid = self.lib.start_consultation(appt_id)
                    print("Consultation recorded. ID:", cid)
                elif ch == '3':
                    appt_id = input("Enter Appointment ID: ").strip()
                    self.lib.prescribe_medicine(appt_id)
                    print("Medicine prescription saved.")
                elif ch == '4':
                    appt_id = input("Enter Appointment ID: ").strip()
                    self.lib.prescribe_lab_test(appt_id)
                    print("Lab tests requested.")
                elif ch == '5':
                    patient_id = input("Enter Patient ID: ").strip()
                    hist = self.lib.view_patient_history(patient_id)
                    print("Consultations:")
                    for c in hist['consultations']:
                        print(f"- {c['CreatedDate']} | {c['Symptoms']} | {c['Diagnosis']}")
                elif ch == '6':
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print("Error:", str(e))
            # Screens/doctor_screen.py  (inside menu try/except blocks)
            except ValidationError as ve:
                print("Invalid input:", ve)
            except PermissionError as pe:
                print("Permission error:", pe)
            except NotFoundError as nf:
                print("Not found:", nf)
            except Exception as e:
                print("Operation failed:", e)

