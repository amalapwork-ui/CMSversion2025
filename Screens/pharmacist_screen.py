# Screens/pharmacist_screen.py
from Lib.PharmacistLib import PharmacistLib

class PharmacistScreen:
    def __init__(self):
        self.lib = PharmacistLib()

    def menu(self):
        while True:
            print("\n=== PHARMACY DASHBOARD ===")
            print("1. Add New Medicine")
            print("2. Update Stock")
            print("3. View Expired Stock")
            print("4. Remove Expired")
            print("5. Dispense Medicine")
            print("6. Verify Prescription")
            print("7. Logout")

            ch = input("Choice: ").strip()
            try:
                if ch == '1':
                    name = input("Name: ")
                    exp = input("Expiry (YYYY-MM-DD): ")
                    cat = input("Category ID: ")
                    mid = self.lib.add_new_medicine(name, exp, cat)
                    print(f"Medicine Added ID: {mid}")

                elif ch == '2':
                    med = input("Medicine ID: ")
                    batch = input("Batch No: ")
                    qty = int(input("Quantity: "))
                    exp = input("Expiry: ")
                    self.lib.update_stock(med, batch, qty, exp)
                    print("Stock updated.")

                elif ch == '3':
                    rows = self.lib.view_expired_stock()
                    for r in rows:
                        print(r)

                elif ch == '4':
                    sid = input("StockId to remove: ")
                    self.lib.remove_expired(sid)
                    print("Removed.")

                # elif ch == '5':
                #     appt = input("Appointment ID: ")
                #     self.lib.dispense_medicines(appt)
                #     print("Dispensed.")
                elif ch == '5':  # Dispense Medicine
                    appt = input(int("Appointment ID: "))
                    # first verify prescription
                    meds = self.lib.verify_prescription(appt)
                    if not meds:
                        print("No medicines prescribed.")
                        continue
                    print("Prescription items:")
                    for m in meds:
                        print(f"{m['MedicinePrescriptionId']} - {m['MedicineName']} | {m['Dosage']} | {m['Frequency']} | {m['Duration']}")
                    if not confirm("Proceed to dispense all medicines for this appointment? (y/n): "):
                        print("Cancelled.")
                        continue
                    try:
                        dispensed = self.lib.dispense_medicines(appt)
                        print("Dispensed:", dispensed)
                    except Exception as e:
                        print("Failed to dispense:", e)

                elif ch == '6':
                    appt = input("Appointment ID: ")
                    meds = self.lib.verify_prescription(appt)
                    for m in meds:
                        print(m)

                elif ch == '7':
                    break

            except Exception as e:
                print("Error:", e)
