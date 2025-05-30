
import random

def game():
    number_to_guess = random.randint(1, 100)
    guess = None
    while guess != number_to_guess:
        guess = int(input("Guess a number between 1 and 100: "))
        if guess < number_to_guess:
            print("Too low!")
        elif guess > number_to_guess:
            print("Too high!")
    print("Congratulations! You won!")

game()
