# Password Manager

A command-line Python application to securely store and manage your passwords.

## Features
- Save passwords for different websites/accounts
- Random password generator (OIBSIP Task 3): choose length (8-64) and character types (uppercase, lowercase, numbers, symbols; at least 2), with input validation
- Generated with Python's `secrets` module (cryptographically secure)
- View saved credentials
- Update or delete saved entries
- Data stored locally in a JSON file

## Tech Used
- Python 3 (`secrets`, `string`, `json`, `re`)
- JSON file storage

## How to Run
1. Clone the repo:
   git clone https://github.com/somaygahlot09/password-manager.git

2. Go into the folder:
   cd password-manager
   
3. Run the program:
   python main.py


## Note
Your saved passwords are stored locally in `passwords.json`, which is excluded from this repository via `.gitignore`. The file is created automatically when you run the program.

## Author
Somay Gahlot