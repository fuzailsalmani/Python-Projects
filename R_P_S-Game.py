import random

print("====== Rock Paper Scissors ======")

option = ("Rock", "Paper", "Scissor")

while True:
    computer = random.choice(option)

    try:
        player = input("Enter your choice (Rock/Paper/Scissor): ").capitalize()

        if player not in option:
            print("Not understood your choice! Please enter a correct choice.")
            continue

    except:
        print("Something went wrong!")
        continue

    print("Your Choice:", player)
    print("Computer Choice:", computer)

    if player == computer:
        print("Match is Draw. Try again!")

    elif (player == "Paper" and computer == "Rock") or \
         (player == "Scissor" and computer == "Paper") or \
         (player == "Rock" and computer == "Scissor"):
        print("You Win!")

    else:
        print("You Lost!")

    choice = input("Do you want to play again? (y/n): ")

    if choice.lower() != "y":
        print("Thank you for playing!")
        break