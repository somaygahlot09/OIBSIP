# This module handles file operations for the password manager application, including loading and saving passwords to a JSON file.

import json
import os
# ---------- Load Passwords(fetching data from json file)---------------

def load_passwords():

    try:

        # Create file if it doesn't exist
        if not os.path.exists("passwords.json"):
            with open("passwords.json", "w") as file:
                json.dump([], file, indent=4)
            return []

        with open("passwords.json", "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Error: JSON file is corrupted.")
        return []

    except FileNotFoundError:
        print("Password file not found.")
        return []

    except Exception as e:
        print("Error loading passwords:", e)
        return []


# ---------- Save Passwords(saving data to json file) ----------

def save_passwords(data):

    try:

        with open("passwords.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Passwords saved successfully.")

    except PermissionError:
        print("Permission denied while saving the file.")

    except Exception as e:
        print("Error saving passwords:", e)