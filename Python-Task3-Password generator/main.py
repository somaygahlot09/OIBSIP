#This is the main module for the password manager application. 
#This module contain of calling operations.

from operations import (
    add_password,
    view_passwords,
    search_password,
    update_password,
    delete_password,
)

from password_utils import generate_password


def menu():

    while True:

        try:

            print("\n========== PASSWORD MANAGER ==========")

            print("""
1. Add Password
2. View Passwords
3. Search Password
4. Update Password
5. Delete Password
6. Generate Password
7. Exit
""")

            choice = input("Enter Choice: ")

            if choice == "1":
                add_password()

            elif choice == "2":
                view_passwords()

            elif choice == "3":
                search_password()

            elif choice == "4":
                update_password()

            elif choice == "5":
                delete_password()

            elif choice == "6":
                generate_password()

            elif choice == "7":
                print("Thank You!")
                break

            else:
                print("Invalid Choice.")

        except KeyboardInterrupt:
            print("\nProgram Interrupted.")
            break

        except Exception as e:
            print("Unexpected Error:", e)


menu()