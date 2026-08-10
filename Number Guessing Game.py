import random

print("Welcome to the Number Guessing Game!")

while True:
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    won = False

    print("\nI have chosen a number between 1 and 100.")

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        attempts += 1

        if guess == secret_number:
            print("Congratulations! You guessed the correct number.")
            print("Total Attempts:", attempts)
            won = True
            break

        elif guess > secret_number:
            print("Too High! Try Again.")

        else:
            print("Too Low! Try Again.")

        print("Attempts left:", max_attempts - attempts)

    if not won:
        print("\nSorry! You've used all 5 attempts.")
        print("The secret number was:", secret_number)

    choice = input("\nDo you want to play again? (y/n): ").lower()

    if choice != "y":
        print("Thank you for playing!")
        break