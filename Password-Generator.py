import random

print("================= Auto Generate Password =================")

lower_case = "qwertyuioplkjhgfdsazxcvbnm"
upper_case = "QWERTYUIOPLKJHGFDSAZXCVBNM"
symbol = "!@#$%^&*()?,;:'+=-_"
number = "1234567890"

characters = lower_case + upper_case + symbol + number

while True:

    try:
        a = int(input("Enter password length (6, 8, 12): "))

        if a not in (6, 8, 12):
            print("Please enter only 6, 8, or 12.")
            continue

        password = ""

        while len(password) < a:
            character = random.choice(characters)
            password = password + character

        print("Congratulations! Your password is:", password)

        again = input("Generate another password? (y/n): ").lower()

        if again != "y":
            print("Thank you for using Password Generator!")
            break

    except ValueError:
        print("Please enter numbers only. Example: 6, 8, 12")