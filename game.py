#TODO: Make a Player and Enemy child class with loot for enemy and inventory for player
#TODO: Make a function that starts a fight
import os

import utility
from utility import Player, clearWindow
from termcolor import colored
import time

# Welcoming message
welcomeMessage = f"This is the {colored("TerminalRPG", "yellow")}! Here you will find basic gameplay but it was made with love!"
for char in welcomeMessage:
    print(char, end="", flush=True)
    time.sleep(.05)
print()
time.sleep(0.5)

instructionMessage = f"In this game all of the {colored("actions", "yellow")} you do are determined by the {colored("terms", "yellow")} you type into the {colored("input field", "yellow")}"
for char in instructionMessage:
    print(char, end="", flush=True)
    time.sleep(.05)
time.sleep(0.5)
print("\nGood Luck!")

