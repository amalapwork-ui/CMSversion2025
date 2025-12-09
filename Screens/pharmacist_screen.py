# # Screens/pharmacist_screen.py
# from Utils.InputUtils import confirm, input_date,input_int,input_str
# from Lib.PharmacistLib import PharmacistLib
# from Exceptions.Errors import AppError

# class PharmacistScreen:
#     def __init__(self):
#         self.lib = PharmacistLib()

#     def menu(self):
#         while True:
#             print("\n=== PHARMACY DASHBOARD ===")
#             print("1. Add New Medicine")
#             print("2. Update Stock")
#             print("3. View Expired Stock")
#             print("4. Remove Expired")
#             print("5. Dispense Medicine")
#             print("6. Verify Prescription")
#             print("7. Logout")

#             ch = input("Choice: ").strip()
#             try:
#                 if ch == '1':
#                     name = input("Medicine Name: ")
#                     exp = input("Expiry (YYYY-MM-DD): ")
#                     mid = self.lib.add_new_medicine(name, exp)
#                     print(f"Medicine Added! ID: {mid}")

#                 elif ch == '2':
#                     med = input("Medicine ID: ")
#                     batch = input("Batch No: ")
#                     qty = int(input("Quantity: "))
#                     exp = input("Expiry: ")
#                     self.lib.update_stock(med, batch, qty, exp)
#                     print("Stock updated.")

#                 elif ch == '3':
#                     rows = self.lib.view_expired_stock()
#                     if not rows:
#                         print("No expired stock found.")
#                     else:
#                         print("------Expired Stock-------")
#                         for r in rows:
#                             print(f"StockId: {r['MedicineStockId']} | Medicine: {r['MedicineId']}")

#                 elif ch == '4':
#                     sid = input("StockId to remove: ")
#                     self.lib.remove_expired(sid)
#                     print("Removed Expired Stock")

#                 # elif ch == '5':
#                 #     appt = input("Appointment ID: ")
#                 #     self.lib.dispense_medicines(appt)
#                 #     print("Dispensed.")
#                 elif ch == '5':  # Dispense Medicine
#                     appt_id = input_int("Appointment ID: ")
#                     # first verify prescription
#                     meds = self.lib.verify_prescription(appt)
#                     if not meds:
#                         print("No medicines prescribed.")
#                         continue
#                     print("Prescription items:")
#                     for m in meds:
#                         print(f"{m['MedicinePrescriptionId']} - {m['MedicineName']} | {m['Dosage']} | {m['Frequency']} | {m['Duration']}")
#                     if not confirm("Proceed to dispense all medicines for this appointment? (y/n): "):
#                         print("Cancelled.")
#                         continue
#                     try:
#                         dispensed = self.lib.dispense_medicines(appt)
#                         print("Dispensed:", dispensed)
#                     except Exception as e:
#                         print("Failed to dispense:", e)

#                 elif ch == '6':
#                     appt = input("Appointment ID: ")
#                     meds = self.lib.verify_prescription(appt)
#                     for m in meds:
#                         print(m)

#                 elif ch == '7':
#                     break

#             except Exception as e:
#                 print("Error:", e)


from Lib.PharmacistLib import PharmacistLib
from Utils.InputUtils import input_str, input_int, input_date, confirm
from Exceptions.Errors import AppError

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

            ch = input_str("Choice: ")

            try:
                if ch == '1':
                    name = input_str("Medicine Name: ")
                    exp = input_date("Expiry (YYYY-MM-DD): ")
                    mid = self.lib.add_new_medicine(name, exp)
                    print(f"✅ Medicine Added! ID: {mid}")

                elif ch == '2':
                    med_id = input_int("Medicine ID: ")
                    batch = input_str("Batch No: ")
                    qty = input_int("Quantity: ")
                    exp = input_date("Expiry (YYYY-MM-DD): ")
                    self.lib.update_stock(med_id, batch, qty, exp)
                    print("✅ Stock updated.")

                elif ch == '3':
                    rows = self.lib.view_expired_stock()
                    if not rows:
                        print("No expired stock found.")
                    else:
                        print("\n--- Expired Stock ---")
                        for r in rows:
                            print(f"StockID: {r['MedicineStockId']} | Med: {r['MedicineId']} | Batch: {r['BatchNo']} | Exp: {r['ExpiryDate']}")

                elif ch == '4':
                    sid = input_int("Enter StockId to remove: ")
                    self.lib.remove_expired(sid)
                    print("✅ Removed.")

                elif ch == '5':  # Dispense Medicine
                    appt_id = input_int("Appointment ID: ")
                    
                    # 1. Verify
                    meds = self.lib.verify_prescription(appt_id)
                    if not meds:
                        print("⚠ No medicines prescribed for this appointment.")
                        continue
                    
                    print("\n--- Prescription ---")
                    for m in meds:
                        print(f"Rx: {m['MedicineName']} | {m['Dosage']} | {m['Frequency']} | {m['Duration']}")
                    
                    # 2. Confirm
                    if confirm("Proceed to dispense? (y/n): "):
                        self.lib.dispense_medicines(appt_id)
                        print("✅ Medicines dispensed & stock updated.")
                    else:
                        print("Cancelled.")

                elif ch == '6':
                    appt_id = input_int("Appointment ID: ")
                    meds = self.lib.verify_prescription(appt_id)
                    if not meds:
                        print("No prescription found.")
                    else:
                        for m in meds:
                            print(f"{m['MedicineName']} - {m['Dosage']}")

                elif ch == '7':
                    break
            
            except AppError as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ System Error: {e}")