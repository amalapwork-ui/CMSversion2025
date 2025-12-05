# Screens/labtech_screen.py
from Lib.LabTechLib import LabTechLib

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

            ch = input("Choice: ").strip()
            try:
                if ch == '1':
                    name = input("Test Name: ")
                    rr = input("Reference Range: ")
                    cat = input("Category ID: ")
                    amt = input("Amount: ")
                    tid = self.lib.add_lab_test(name, rr, cat, amt)
                    print("Lab test added:", tid)

                elif ch == '2':
                    rows = self.lib.view_pending_tests()
                    for r in rows:
                        print(r)

                elif ch == '3':
                    pid = input("Prescription ID: ")
                    value = input("Measured Value: ")
                    result = input("Result (Normal/Abnormal): ")
                    remarks = input("Remarks: ")
                    self.lib.record_result(pid, value, result, remarks)
                    print("Recorded.")

                elif ch == '4':
                    break

            except Exception as e:
                print("Error:", e)
