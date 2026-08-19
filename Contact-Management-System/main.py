import json
import os


# ==================== LOAD DATA ====================

def load_data():
    if os.path.exists("details.json"):
        with open("details.json", "r") as file:
            return json.load(file)

    return {}


# ==================== SAVE DATA ====================

def save_data(details):
    with open("details.json", "w") as file:
        json.dump(details, file, indent=4)


# ==================== CREATE ACCOUNT ====================

def create_account(details):
    user_id = input("Enter User ID: ")

    if user_id in details:
        print("User ID already exists!")
        return

    while True:
        password = input("Create a strong password: ")

        # Password length validation
        if len(password) < 8 or len(password) > 12:
            print("Password must be between 8 and 12 characters.")
            continue

        # Check for at least one digit
        has_digit = False

        for char in password:
            if char.isdigit():
                has_digit = True
                break

        if not has_digit:
            print("Password must contain at least one digit.")
            continue

        # Check for at least one uppercase letter
        has_upper = False

        for char in password:
            if char.isupper():
                has_upper = True
                break

        if not has_upper:
            print("Password must contain at least one uppercase letter.")
            continue

        # Check for at least one special character
        has_special = False

        for char in password:
            if not char.isalnum():
                has_special = True
                break

        if not has_special:
            print("Password must contain at least one special character.")
            continue

        print("Password is valid!")
        break

    # Store account details
    details[user_id] = {
        "password": password,
        "contacts": {}
    }

    save_data(details)

    print("Account created successfully!")


# ==================== LOGIN ====================

def login(details):
    user_id = input("Enter your User ID: ")

    if user_id not in details:
        print("User not found!")
        return

    attempt = 1
    login_success = False

    while attempt <= 3:
        password = input("Enter your password: ")

        if password == details[user_id]["password"]:
            print("Login successful!")
            login_success = True
            break

        print("Incorrect password!")
        print("Attempts remaining:", 3 - attempt)

        attempt += 1

    if not login_success:
        print("Too many failed attempts!")
        print("Login blocked!")
        return

    contact_menu(details, user_id)


# ==================== ADD CONTACT ====================

def add_contact(details, user_id):

    while True:
        name = input("Enter contact name: ")

        if name in details[user_id]["contacts"]:
            print("Contact already exists!")
            continue

        phone_number = input("Enter phone number: ")

        details[user_id]["contacts"][name] = phone_number

        save_data(details)

        print("Contact saved successfully!")
        break


# ==================== VIEW CONTACTS ====================

def view_contacts(details, user_id):

    if not details[user_id]["contacts"]:
        print("No contacts found!")

    else:
        print("\n===== Your Contacts =====")

        for name, phone in details[user_id]["contacts"].items():
            print(name, ":", phone)


# ==================== UPDATE CONTACT ====================

def update_contact(details, user_id):

    name = input("Enter contact name: ")

    if name not in details[user_id]["contacts"]:
        print("Contact not found!")

    else:
        new_phone_number = input("Enter new phone number: ")

        details[user_id]["contacts"][name] = new_phone_number

        save_data(details)

        print("Contact updated successfully!")


# ==================== DELETE CONTACT ====================

def delete_contact(details, user_id):

    name = input("Enter contact name: ")

    if name not in details[user_id]["contacts"]:
        print("Contact not found!")

    else:
        del details[user_id]["contacts"][name]

        save_data(details)

        print("Contact deleted successfully!")


# ==================== CONTACT MENU ====================

def contact_menu(details, user_id):

    while True:
        print("\n===== Contact Management =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Logout")

        contact_choice = int(input("Enter your choice: "))

        if contact_choice == 1:
            add_contact(details, user_id)

        elif contact_choice == 2:
            view_contacts(details, user_id)

        elif contact_choice == 3:
            update_contact(details, user_id)

        elif contact_choice == 4:
            delete_contact(details, user_id)

        elif contact_choice == 5:
            print("Logged out successfully!")
            break

        else:
            print("Invalid choice! Please try again.")


# ==================== MAIN PROGRAM ====================

details = load_data()

while True:
    print("\n===== Contact Management System =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        create_account(details)

    elif choice == 2:
        login(details)

    elif choice == 3:
        print("Thank you for using the Contact Management System!")
        break

    else:
        print("Invalid choice! Please try again.")