
# # main.py (entry)
# from Lib.AuthLib import AuthLib
# from Screens.doctor_screen import DoctorScreen
# from Screens.reception_screen import ReceptionScreen
# from Screens.pharmacist_screen import PharmacistScreen
# from Screens.labtech_screen import LabTechScreen
# from Screens.admin_screen import AdminScreen

# # import other screens as added

# def main():
#     auth = AuthLib()
#     print("=== CMS LOGIN ===")
#     username = input("Username: ").strip()
#     password = input("Password: ").strip()

#     session = auth.login(username, password)
#     if not session:
#         print("Invalid credentials.")
#         return

#     role = session.get('role_name', '').lower()
#     print(f"Welcome {session.get('full_name')} - Role: {session.get('role_name')}")

#     if role == 'doctor':
#         doctor_id = session.get('doctor_id')
#         if not doctor_id:
#             print("Doctor profile not linked to this staff account.")
#             return
#         DoctorScreen(doctor_id).menu()
#     elif role == 'receptionist':
#         ReceptionScreen().menu()

#     elif role == 'pharmacist':
#         PharmacistScreen().menu()

#     elif role == 'lab technician':
#         LabTechScreen().menu()

#     elif role == 'admin':
#         AdminScreen().menu()



#     else:
#         print("Role not implemented in this demo. Implement screens and libs for other roles.")

# if __name__ == "__main__":
#     main()


# main.py
from Lib.AuthLib import AuthLib
from Screens.admin_screen import AdminScreen
from Screens.doctor_screen import DoctorScreen
from Screens.reception_screen import ReceptionScreen
from Screens.pharmacist_screen import PharmacistScreen
from Screens.labtech_screen import LabTechScreen

def main():
    print("=================================")
    print("     CLINICAL MANAGEMENT SYSTEM  ")
    print("=================================")

    auth = AuthLib()

    while True:
        print("\n=== LOGIN ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        session = auth.login(username, password)
        if not session:
            print("\n❌ Invalid credentials. Try again.\n")
            continue

        print(f"\n✅ Welcome {session['full_name']} ({session['role_name']})")

        role = session['role_name'].lower()

        # -------- ROUTE TO MODULE ----------
        if role == 'admin':
            AdminScreen().menu()

        elif role == 'doctor':
            if session.get('doctor_id') is None:
                print("\n⚠ No doctor profile linked to this staff account.")
            else:
                DoctorScreen(session['doctor_id']).menu()

        elif role == 'receptionist':
            ReceptionScreen().menu()

        elif role == 'pharmacist':
            PharmacistScreen().menu()

        elif role == 'lab technician':
            LabTechScreen().menu()

        else:
            print("\n Unknown role assigned. Contact admin.")
        
        # -------- AFTER LOGOUT ----------
        print("\nYou have been logged out.")
        l_again = input("Login again? (y/n): ").strip().lower()
        if l_again != 'y':
            break

    print("\nThank you for using CMS. Goodbye!")

if __name__ == "__main__":
    main()

