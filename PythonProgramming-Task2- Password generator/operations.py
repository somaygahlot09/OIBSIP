#This is the module that contains main operations(add,view,search,update,delete) for the password manager application.

from file_handler import load_passwords, save_passwords
from password_utils import generate_password
from validator import validate_website

def add_password():
    

    try:

        data = load_passwords()

        website = input("Website : ").strip()
        username = input("Username: ").strip()

        if website == "" or username == "":
            print("Fields cannot be empty.")
            return

        if not validate_website(website):
            print("Invalid website URL.")
            return

        choice = input("Generate password? (y/n): ").lower()

        if choice == "y":
            password = generate_password()

        elif choice == "n":
            password = input("Enter Password: ")

        else:
            print("Invalid choice.")
            return

        data.append(
            {
                "Website": website,
                "Username": username,
                "Password": password,
            }
        )

        save_passwords(data)

        print("Password saved successfully.")

    except Exception as e:
        print("Error:", e)


def view_passwords():

    try:

        data = load_passwords()

        if not data:
            print("No passwords found.")
            return

        print("\n------ PASSWORDS ------")

        for i, item in enumerate(data, start=1):

            print(f"\nID : {i}")
            print("Website :", item["Website"])
            print("Username:", item["Username"])
            print("Password:", item["Password"])

    except Exception as e:
        print("Error:", e)


def search_password():

    try:

        data = load_passwords()

        website = input("Enter Website: ").lower()

        for item in data:

            if item["Website"].lower() == website:

                print("\nFound")

                print("Website :", item["Website"])
                print("Username:", item["Username"])
                print("Password:", item["Password"])

                return

        print("Website not found.")

    except Exception as e:
        print("Error:", e)


def update_password():

    try:

        data = load_passwords()

        website = input("Enter Website: ")

        for item in data:

            if item["Website"].lower() == website.lower():

                choice = input("Generate new password? (y/n): ").lower()

                if choice == "y":
                    item["Password"] = generate_password()
                elif choice == "n":
                    item["Password"] = input("New Password: ")
                else:
                    print("Invalid choice.")
                    return

                save_passwords(data)

                print("Password Updated.")

                return

        print("Website not found.")

    except Exception as e:
        print("Error:", e)


def delete_password():

    try:

        data = load_passwords()

        website = input("Enter Website: ")

        for item in data:

            if item["Website"].lower() == website.lower():

                data.remove(item)

                save_passwords(data)

                print("Password Deleted.")

                return

        print("Website not found.")

    except Exception as e:
        print("Error:", e)