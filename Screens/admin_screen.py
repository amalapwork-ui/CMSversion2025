# Screens/admin_screen.py
from Lib.AdminLib import AdminLib
from Exceptions.Errors import ValidationError


class AdminScreen:
    def __init__(self):
        self.lib = AdminLib()

    def menu(self):
        while True:
            print("\n=== ADMIN DASHBOARD ===")
            print("1. Manage Staff")
            print("2. Manage Roles")
            print("3. Manage Specializations")
            print("4. Manage Doctor Profiles")
            print("5. Logout")

            choice = input("Enter choice: ")

            if choice == '1':
                self.manage_staff()
            elif choice == '2':
                self.manage_roles()
            elif choice == '3':
                self.manage_specializations()
            elif choice == '4':
                self.manage_doctor_profiles()
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

    # ---------------- STAFF -------------------
    def manage_staff(self):
        while True:
            print("\n1. Add Staff\n2. Update Staff\n3. Deactivate Staff\n4. Reactivate Staff\n5. View All Staff Profiles\n 6. Back")
            ch = input("Choice: ")
            try:
                if ch == '1':
                    fullname = input("Full Name: ")
                    gender = input("Gender: ")
                    joining = input("Joining Date (YYYY-MM-DD): ")
                    mobile = input("Mobile: ")
                    username = input("Username: ")
                    password = input("Password: ")
                    role_id = input("Role ID: ")
                    sid = self.lib.add_staff(fullname, gender, joining, mobile, username, password, role_id)
                    print("Created Staff ID:", sid)

                elif ch == '2':
                    sid = input("Staff ID: ")
                    fullname = input("New Name: ")
                    gender = input("New Gender: ")
                    mobile = input("New Mobile: ")
                    role_id = input("New Role ID: ")
                    self.lib.update_staff(sid, fullname, gender, mobile, role_id)
                    print("Updated Staff Profile")

                elif ch == '3':
                    sid = input("Staff ID: ")
                    self.lib.deactivate_staff(sid)
                    print("Deactivated Staff Profile")

                elif ch == '4':
                    sid = input("Staff ID: ")
                    self.lib.reactivate_staff(sid)
                    print("Reactivated Staff Profile")

                # elif ch == '5': 
                #     rows = self.lib.get_all_staff()
                #     if not rows:
                #         print("No staff records found.")
                #     else:
                #         # 1. Print the Header
                #         print(f"\n{'ID':<5} {'Name':<20} {'Gender':<8} {'Mobile':<15} {'Joined':<12} {'RoleID'}")
                #         print("-" * 75) # A distinct separator line
                        
                #         # 2. Print the Rows
                #         for r in rows:
                #             print(f"{r['StaffId']:<5} {r['FullName']:<20} {r['Gender']:<8} {r['MobileNumber']:<15} {str(r['JoiningDate']):<12} {r['RoleId']}")
                #         print("-" * 75)
                elif ch == '5':
                    rows = self.lib.get_all_staff()
                    if not rows:
                        print("No staff records found.")
                    else:
                        # 1. Update Header to show 'Role' instead of 'RoleID'
                        print(f"\n{'ID':<5} {'Name':<20} {'Gender':<8} {'Mobile':<15} {'Joined':<12} {'Role'}")
                        print("-" * 80)
                        
                        # 2. Update Row Printing
                        for r in rows:
                            # distinct 'Yes'/'No' for active status if you want, or just leave it out
                            print(f"{r['StaffId']:<5} {r['FullName']:<20} {r['Gender']:<8} {r['MobileNumber']:<15} {str(r['JoiningDate']):<12} {r['RoleName']}")
                        print("-" * 80)
                elif ch == '6':
                    break
            except Exception as e:
                print("Error: ",e)
    # ---------------- ROLES -------------------
    def manage_roles(self):
        while True:
            print("\n1. Add Role\n2. Update Role\n3. View All Roles\n4. Back")
            ch = input("Choice: ")
            try:
                if ch == '1':
                    name = input("Role name: ")
                    rid = self.lib.add_role(name)
                    print("Role created:", rid)
                elif ch == '2':
                    rid = input("Role ID: ")
                    name = input("New Role Name: ")
                    self.lib.update_role(rid, name)
                    print("Updated Role details")
                # elif ch == '3':
                #     rows = self.lib.get_roles()
                #     for r in rows:
                #         print(r)
                elif ch == '3':
                    rows = self.lib.get_roles()
                    if not rows:
                        print("No roles defined.")
                    else:
                        # 1. Print Header
                        print(f"\n{'ID':<5} {'Role Name':<20}")
                        print("-" * 30)
                        
                        # 2. Print Rows
                        for r in rows:
                            print(f"{r['RoleId']:<5} {r['RoleName']:<20}")
                        print("-" * 30)
                elif ch == '4':
                    break

            except Exception as e:
                print("Error: ", e)

        # ---------------- SPECIALIZATION -------------------
        # def manage_specializations(self):
        #     print("\n1. Add\n2. Update\n3. Deactivate\n4. Reactivate\n5. View All")
        #     ch = input("Choice: ")

        #     if ch == '1':
        #         name = input("Name: ")
        #         sid = self.lib.add_specialization(name)
        #         print("Created:", sid)
        #     elif ch == '2':
        #         sid = input("Spec ID: ")
        #         name = input("New name: ")
        #         self.lib.update_specialization(sid, name)
        #         print("Updated.")
        #     elif ch == '3':
        #         sid = input("Spec ID: ")
        #         self.lib.deactivate_specialization(sid)
        #         print("Deactivated.")
        #     elif ch == '4':
        #         sid = input("Spec ID: ")
        #         self.lib.reactivate_specialization(sid)
        #         print("Reactivated.")
        #     elif ch == '5':
        #         rows = self.lib.get_all_specializations()
        #         for r in rows:
        #             print(r)

    # ---------------- SPECIALIZATION -------------------
    def manage_specializations(self):
        while True:
            print("\n=== MANAGE SPECIALIZATIONS ===")
            print("1. Add Specialization")
            print("2. Update Specialization")
            print("3. Deactivate Specialization")
            print("4. Reactivate Specialization")
            print("5. View All Specializations")
            print("6. Back")

            ch = input("Choice: ").strip()

            try:
                if ch == '1':
                    name = input("New Specialization Name: ").strip()
                    sid = self.lib.add_specialization(name)
                    print(f"Specialization added with ID: {sid}")

                elif ch == '2':
                    # SHOW LIST BEFORE ASKING
                    self.show_specialization_list()

                    spec_id = input("Enter Specialization ID to update: ").strip()
                    new_name = input("Enter new specialization name: ").strip()
                    self.lib.update_specialization(spec_id, new_name)
                    print("Specialization updated.")

                elif ch == '3':
                    self.show_specialization_list()
                    sid = input("Enter Specialization ID to deactivate: ").strip()
                    self.lib.deactivate_specialization(sid)
                    print("Specialization deactivated.")

                elif ch == '4':
                    self.show_specialization_list()
                    sid = input("Enter Specialization ID to reactivate: ").strip()
                    self.lib.reactivate_specialization(sid)
                    print("Specialization reactivated.")

                elif ch == '5':
                    self.show_specialization_list()

                elif ch == '6':
                    break

                else:
                    print("Invalid choice.")

            except Exception as e:
                print("Error:", e)


    def show_specialization_list(self):
        specs = self.lib.get_all_specializations()

        if not specs:
            print("\n⚠ No specializations found.")
            return

        print("\nAvailable Specializations:")
        print("--------------------------")
        for s in specs:
            print(f"ID: {s['SpecializationId']}  |  Name: {s['SpecializationName']}  |  Active: {s['IsActive']}")
        print("--------------------------")

        


    # ---------------- DOCTOR PROFILE -------------------
    # def manage_doctor_profiles(self):
    #     print("\n1. Add Doctor Profile\n2. Update Doctor Profile\n3. Deactivate\n4. Reactivate")
    #     ch = input("Choice: ")

    #     if ch == '1':
    #         staff_id = input("Staff ID: ")
    #         spec_id = input("Specialization ID: ")
    #         fee = input("Consultation Fee: ")
    #         did = self.lib.create_doctor_profile(staff_id, spec_id, fee)
    #         print("Doctor created:", did)

    #     elif ch == '2':
    #         did = input("Doctor ID: ")
    #         spec_id = input("New Specialization ID: ")
    #         fee = input("New Fee: ")
    #         # self.lib.update_doctor(did, spec_id, fee)
    #         # print("Updated.")
    #         try:
    #             self.lib.update_doctor(did, spec_id, fee)
    #             print("Doctor updated successfully.")
    #         except ValidationError as ve:
    #             print("Error:", ve)
    #         except Exception as e:
    #             print("Unexpected Error:", e)

            

    #     elif ch == '3':
    #         did = input("Doctor ID: ")
    #         self.lib.deactivate_doctor(did)
    #         print("Deactivated.")

    #     elif ch == '4':
    #         did = input("Doctor ID: ")
    #         self.lib.reactivate_doctor(did)
    #         print("Reactivated.")
     # ---------------- DOCTOR PROFILE -------------------
    def manage_doctor_profiles(self):
        while True:
            print("\n=== MANAGE DOCTOR PROFILES ===")
            print("1. Add Doctor Profile")
            print("2. Update Doctor Profile")
            print("3. Deactivate Doctor")
            print("4. Reactivate Doctor")
            print("5. View all Doctor profiles")
            print("6. Back")

            ch = input("Choice: ").strip()

            try:
                if ch == '1':

                    staff_id = input("Enter Staff ID (Doctor): ").strip()
                    spec_id = input("Enter Specialization ID: ").strip()
                    fee = input("Enter Consultation Fee: ").strip()

                    did = self.lib.create_doctor_profile(staff_id, spec_id, fee)
                    print(f"Doctor profile created with ID: {did}")

                elif ch == '2':
                    self.show_specialization_list()

                    did = input("Enter Doctor ID: ").strip()
                    spec_id = input("New Specialization ID: ").strip()
                    fee = input("New Consultation Fee: ").strip()

                    self.lib.update_doctor(did, spec_id, fee)
                    print("Doctor profile updated successfully.")

                elif ch == '3':
                    did = input("Enter Doctor ID to deactivate: ").strip()
                    self.lib.deactivate_doctor(did)
                    print("Doctor deactivated.")

                elif ch == '4':
                    did = input("Enter Doctor ID to reactivate: ").strip()
                    self.lib.reactivate_doctor(did)
                    print("Doctor reactivated.")

                elif ch == '5':
                    rows = self.lib.get_all_doctors()
                    if not rows:
                        print("No doctor profiles found.")
                    else:
                        print(f"\n{'ID':<5} {'Doctor Name':<20} {'Specialization':<20} {'Fee':<10} {'Active'}")
                        print("-" * 70)
                        for r in rows:
                            # 'Yes' if IsActive is 1 else 'No' for cleaner output
                            active_status = "Yes" if r['IsActive'] == 1 else "No"
                            print(f"{r['DoctorId']:<5} {r['FullName']:<20} {r['SpecializationName']:<20} {r['ConsultationFee']:<10} {active_status}")
                        print("-" * 70)

                elif ch == '6':
                    break

                else:
                    print("Invalid choice.")

            except Exception as e:
                print("Error:", e)
