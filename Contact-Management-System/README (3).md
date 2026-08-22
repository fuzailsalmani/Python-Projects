# 📞 Contact Management System

A command-line based Contact Management System built using Python. This project allows users to create accounts, securely log in, and manage their personal contacts.

The application uses **JSON file storage** to save user accounts and contacts, so the data remains available even after the program is closed.

---

## 🚀 Features

### 👤 Account Management

- Create a new account
- Unique User ID validation
- Strong password validation
- Login system with a maximum of 3 attempts
- Change password
- Delete account
- Secure logout

### 🔐 Password Validation

The password must:

- Be between 8 and 12 characters long
- Contain at least one digit
- Contain at least one uppercase letter
- Contain at least one lowercase letter
- Contain at least one special character

---

## 📞 Contact Management

After logging in, users can:

- Add a new contact
- View all saved contacts
- Search for a contact
- Update a contact
- Delete a contact
- Manage only their own contacts

Each user's contacts are stored separately to help maintain privacy.

---

## 💾 Data Storage

This project uses a JSON file named:

```text
details.json
```

The data is automatically:

- Loaded when the program starts
- Saved after creating an account
- Saved after adding a contact
- Saved after updating a contact
- Saved after deleting a contact
- Saved after changing a password
- Updated after deleting an account

Example JSON structure:

```json
{
    "username": {
        "password": "Example@123",
        "contacts": {
            "Ali": "9876543210",
            "Ahmed": "9123456780"
        }
    }
}
```

---

## 🛠️ Technologies Used

- Python
- Functions
- Dictionaries
- Nested Dictionaries
- Loops
- Conditional Statements
- Exception Handling
- File Handling
- JSON
- Python Modules

---

## 📂 Project Structure

```text
Contact-Management-System/
│
├── main.py
├── details.json
└── README.md
```

---

## 📋 Main Menu

```text
===== CONTACT MANAGEMENT SYSTEM =====

1. Create Account
2. Login
3. Exit
```

---

## 📱 Contact Management Menu

After successfully logging in:

```text
===== CONTACT MANAGEMENT =====

1. Add Contact
2. View Contacts
3. Search Contact
4. Update Contact
5. Delete Contact
6. Change Password
7. Delete Account
8. Logout
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Open the project folder

```bash
cd Contact-Management-System
```

### 3. Run the program

```bash
python main.py
```

---

## 🧠 Concepts Practiced

This project was created to practice and improve the following Python concepts:

- Function creation and function calls
- Parameters and arguments
- Return values
- `if`, `elif`, and `else`
- `while` and `for` loops
- `break` and `continue`
- Dictionaries
- Nested dictionaries
- File handling
- JSON data storage
- Exception handling using `try-except`
- Input validation

---

## 🔮 Future Improvements

Possible improvements for future versions:

- Password hashing for better security
- Phone number validation
- Email support for contacts
- Contact sorting
- Search contacts by phone number
- Graphical User Interface (GUI)
- Database integration using SQLite or MySQL

---

## ⚠️ Note

This project is created for learning and practice purposes.

Passwords are currently stored as plain text in the JSON file. In a real-world application, passwords should be securely hashed before storage.

---

## 👨‍💻 Author

**Fuzail Salmani**

---

⭐ If you like this project, consider giving it a star!
