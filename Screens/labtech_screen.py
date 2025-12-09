# # Screens/labtech_screen.py
# from Lib.LabTechLib import LabTechLib

# class LabTechScreen:
#     def __init__(self):
#         self.lib = LabTechLib()

#     def menu(self):
#         while True:
#             print("\n=== LAB TECHNICIAN DASHBOARD ===")
#             print("1. Add Lab Test")
#             print("2. View Pending Tests")
#             print("3. Record Test Result")
#             print("4. Logout")

#             ch = input("Choice: ").strip()
#             try:
#                 if ch == '1':
#                     name = input("Test Name: ")
#                     rr = input("Reference Range: ")
#                     amt = input("Amount: ")
#                     tid = self.lib.add_lab_test(name, rr, amt)
#                     print("Lab test added:", tid)

#                 elif ch == '2':
#                     rows = self.lib.view_pending_tests()
#                     for r in rows:
#                         print(r)

#                 elif ch == '3':
#                     pid = input("Prescription ID: ")
#                     value = input("Measured Value: ")
#                     result = input("Result (Normal/Abnormal): ")
#                     remarks = input("Remarks: ")
#                     self.lib.record_result(pid, value, result, remarks)
#                     print("Recorded.")

#                 elif ch == '4':
#                     break

#             except Exception as e:
#                 print("Error:", e)


from Lib.LabTechLib import LabTechLib
from Utils.InputUtils import input_str, input_int, confirm
from Exceptions.Errors import AppError

class LabTechScreen:
    def __init__(self):
        self.lib = LabTechLib()

    def menu(self):
        while True:
            print("\n=== LAB TECHNICIAN DASHBOARD ===")
            print("1. Add Lab Test")
            print("2. View Pending Tests")
            print("3. Record Test Result")
            print("4. Logout")

            ch = input_str("Choice: ")

            try:
                if ch == '1':
                    name = input_str("Test Name: ")
                    rr = input_str("Reference Range (e.g. 70-100): ")
                    amt = input_int("Cost Amount: ")
                    tid = self.lib.add_lab_test(name, rr, amt)
                    print(f"✅ Lab test added! ID: {tid}")

                elif ch == '2':
                    rows = self.lib.view_pending_tests()
                    if not rows:
                        print("No pending tests.")
                    else:
                        print("\n--- Pending Tests ---")
                        for r in rows:
                            print(f"PrescriptionID: {r['LabTestPrescriptionId']} | Test: {r['TestName']} | Patient: {r['PatientName']}")

                elif ch == '3':
                    pid = input_int("Enter Prescription ID: ")
                    val = input_str("Measured Value: ")
                    res = input_str("Result (Normal/Abnormal): ")
                    rem = input_str("Remarks: ", required=False)
                    
                    self.lib.record_result(pid, val, res, rem)
                    print("✅ Result saved.")

                elif ch == '4':
                    break

            except AppError as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ System Error: {e}")