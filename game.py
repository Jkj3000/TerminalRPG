from utility import *
from termcolor import colored
import time

class Game:
    def __init__(self, playerStats):
        # Initialise all variables
        self.running = True
        self.player = Player(playerStats)

        self.mainScene = Main(self)
        self.shopScene = Shop(self)
        self.adventure = Adventure(self)

        self.scenes = {
            "main": self.mainScene,
            "shop": self.shopScene,
            "adventure": self.adventure
        }
        self.currentScene = self.scenes["main"]

        self.globalActions = {
            "help": self.show_help,
            "quit": self.quit_game
        }

    def enter_screen(self, sceneName):
        # Transition to a different screen
        if sceneName in self.scenes:
            self.currentScene = self.scenes[sceneName]
        else:
            print(f"Screen '{sceneName}' not found!")

    def process_action(self, user_input):
        """Parse and execute action"""
        user_input = user_input.strip().lower()

        if not user_input:
            return

        parts = user_input.split(maxsplit=1)
        action = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        # Check global commands first
        if action in self.globalActions:
            self.globalActions[action](args)
        else:
            # Pass to current screen
            self.currentScene.handleAction(action, args)

    def show_help(self, args):
        print("\nGlobal commands: quit, help")
        print("Type commands based on your current screen.\n")

    def quit_game(self, args):
        print("Thanks for playing!")
        self.running = False

    def game_loop(self):
        """Main game loop"""
        print(colored("Terminal RPG", "yellow"))

        while self.running:
            try:
                self.currentScene.display()
                user_input = input(">> ").strip()
                self.process_action(user_input)
            except KeyboardInterrupt:
                print("\n\nGame interrupted!")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")



if __name__ == "__main__":
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

    statInput = "But first we need you to enter your stats as a player"
    for char in statInput:
        print(char, end="", flush=True)
        time.sleep(.05)
    print("")

    # Making stats
    statsToEnter = ["HP", "DMG", "DEF"]
    completedStats = {}
    for stat in statsToEnter:
        completedStats[stat] = int(input(f"Enter {stat}: "))

    game = Game(completedStats)
    game.game_loop()