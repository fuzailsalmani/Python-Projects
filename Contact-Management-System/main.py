import json
import os


# ==================== FILE CONFIGURATION ====================

FILE_NAME = "details.json"


# ==================== LOAD DATA ====================

def load_data():
    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return {}


# ==================== SAVE DATA ====================

def save_data(details):
    with open(FILE_NAME, "w") as file:
        json.dump(details, file, indent=4)


# ==================== PASSWORD VALIDATION ====================

def validate_password():
    while True:
        password = input("Create a strong password: ")

        # Check password length
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

        # Check for at least one lowercase letter
        has_lower = False

        for char in password:
            if char.islower():
                has_lower = True
                break

        if not has_lower:
            print("Password must contain at least one lowercase letter.")
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

        return password


# ==================== CREATE ACCOUNT ====================

def create_account(details):
    user_id = input("Enter User ID: ").strip()

    if not user_id:
        print("User ID cannot be empty.")
        return

    if user_id in details:
        print("User ID already exists.")
        return

    password = validate_password()

    details[user_id] = {
        "password": password,
        "contacts": {}
    }

    save_data(details)

    print("Account created successfully!")


# ==================== LOGIN ====================

def login(details):
    user_id = input("Enter your User ID: ").strip()

    if user_id not in details:
        print("User not found.")
        return

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        password = input("Enter your password: ")

        if password == details[user_id]["password"]:
            print("Login successful!")
            contact_menu(details, user_id)
            return

        remaining_attempts = max_attempts - attempt

        print("Incorrect password.")

        if remaining_attempts > 0:
            print(f"Attempts remaining: {remaining_attempts}")

    print("Too many failed attempts. Login blocked.")


# ==================== ADD CONTACT ====================

def add_contact(details, user_id):
    contacts = details[user_id]["contacts"]

    while True:
        name = input("Enter contact name: ").strip()

        if not name:
            print("Contact name cannot be empty.")
            continue

        if name in contacts:
            print("Contact already exists. Please enter a different name.")
            continue

        phone_number = input("Enter phone number: ").strip()

        if not phone_number:
            print("Phone number cannot be empty.")
            continue

        contacts[name] = phone_number

        save_data(details)

        print("Contact saved successfully!")
        return


# ==================== VIEW CONTACTS ====================

def view_contacts(details, user_id):
    contacts = details[user_id]["contacts"]

    if not contacts:
        print("No contacts found.")
        return

    print("\n===== YOUR CONTACTS =====")

    for number, (name, phone) in enumerate(contacts.items(), start=1):
        print(f"{number}. {name}: {phone}")


# ==================== SEARCH CONTACT ====================

def search_contact(details, user_id):
    contacts = details[user_id]["contacts"]

    if not contacts:
        print("No contacts available to search.")
        return

    search_name = input("Enter the contact name to search: ").strip()

    if search_name in contacts:
        print(f"Contact found: {search_name} - {contacts[search_name]}")
    else:
        print("Contact not found.")


# ==================== UPDATE CONTACT ====================

def update_contact(details, user_id):
    contacts = details[user_id]["contacts"]

    if not contacts:
        print("No contacts available to update.")
        return

    name = input("Enter the contact name to update: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    new_phone_number = input("Enter the new phone number: ").strip()

    if not new_phone_number:
        print("Phone number cannot be empty.")
        return

    contacts[name] = new_phone_number

    save_data(details)

    print("Contact updated successfully!")


# ==================== DELETE CONTACT ====================

def delete_contact(details, user_id):
    contacts = details[user_id]["contacts"]

    if not contacts:
        print("No contacts available to delete.")
        return

    name = input("Enter the contact name to delete: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    # Confirmation
    confirm = input(
        f"Are you sure you want to delete {name}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        del contacts[name]

        save_data(details)

        print("Contact deleted successfully!")

    else:
        print("Contact deletion cancelled.")


# ==================== CHANGE PASSWORD ====================

def change_password(details, user_id):
    current_password = input("Enter your current password: ")

    if current_password != details[user_id]["password"]:
        print("Incorrect password.")
        return

    print("Create a new password.")
    new_password = validate_password()

    details[user_id]["password"] = new_password

    save_data(details)

    print("Password changed successfully!")


# ==================== DELETE ACCOUNT ====================

def delete_account(details, user_id):
    password = input(
        "Enter your password to delete your account: "
    )

    if password != details[user_id]["password"]:
        print("Incorrect password. Account deletion cancelled.")
        return False

    print("\nWARNING: This will permanently delete your account and all contacts.")

    confirm = input(
        "Are you sure you want to continue? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("Account deletion cancelled.")
        return False

    del details[user_id]

    save_data(details)

    print("Account deleted successfully!")
    print("You have been logged out.")

    return True


# ==================== CONTACT MENU ====================

def contact_menu(details, user_id):
    while True:
        print("\n===== CONTACT MANAGEMENT =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Change Password")
        print("7. Delete Account")
        print("8. Logout")

        try:
            contact_choice = int(input("Enter your choice: "))

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if contact_choice == 1:
            add_contact(details, user_id)

        elif contact_choice == 2:
            view_contacts(details, user_id)

        elif contact_choice == 3:
            search_contact(details, user_id)

        elif contact_choice == 4:
            update_contact(details, user_id)

        elif contact_choice == 5:
            delete_contact(details, user_id)

        elif contact_choice == 6:
            change_password(details, user_id)

        elif contact_choice == 7:
            account_deleted = delete_account(details, user_id)

            if account_deleted:
                break

        elif contact_choice == 8:
            print("Logged out successfully!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


# ==================== MAIN PROGRAM ====================

def main():
    details = load_data()

    while True:
        print("\n===== CONTACT MANAGEMENT SYSTEM =====")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice: "))

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            create_account(details)

        elif choice == 2:
            login(details)

        elif choice == 3:
            print("Thank you for using the Contact Management System!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


# ==================== START PROGRAM ====================

if __name__ == "__main__":
    main()
