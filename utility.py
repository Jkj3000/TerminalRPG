from beautifultable import BeautifulTable
from termcolor import colored
import os
from abc import ABC, abstractmethod


# Support Functions
def make_dictionary_table(dictionary):
    if type(dictionary) == dict:
        table = BeautifulTable()
        table.columns.header = ["Stat", "Value"]
        for key, value in dictionary.items():
            table.rows.append([key, colored(value, "red")])
        return table
    elif type(dictionary) == list:
        pass

def clear_window():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def compare_stats(stat1, stat2):
    if stat1 > stat2:
        return True
    else:
        return False





# Creatutes
class Creature:
    def __init__(self, statsDict, inventoryDict=[]):
        self.stats = statsDict
        self.inventoryDict = inventoryDict

    def accesStat(self, statKey):
        for key in self.stats:
            if statKey in key:
                return self.stats[key]

    def accesInventoryDict(self, index):
        return self.inventoryDict[index]

class Player(Creature):
    pass

class Enemy(Creature):
    pass





# Scene classes
class Scene(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def handleAction(self, command, args=""):
        pass

class Main(Scene):
    def __init__(self, game):
        super().__init__(game)
    def display(self):
        print(colored("---Main Screen---", "yellow"))
        print("Commands: adventure, shop, city, quit")
        print(make_dictionary_table(self.game.player.stats))

    def handleAction(self, command, args=""):
        if command == "adventure":
            self.game.enter_scene("adventure")
        if command == "shop":
            self.game.enter_scene("shop")
        if command == "city":
            self.game.enter_scene("city")
        if command == "stats":
            make_dictionary_table(self.game.player.stats)

class Shop(Scene):
    listOfShopItems = [
        {"Basic Sword": 10},
        {"Medium Sword": 100},
        {"Epic Sword": 500},
        {"Legendary Sword": 5000},
        {"Basic Shield": 100},
        {"Medium Shield": 500},
        {"Epic Shield": 5000},
        {"Legendary Shield": 8000},
    ]

    def __init__(self, game):
        self.shopDict = {}
        super().__init__(game)

    def display(self):
        # Text

        make_dictionary_table(self.shopDict)
        print(colored("---Shop---", "yellow"))
        print("Commands: main, buy 1-n, inventory")
        print("How to purchase:\nType 1-n to purchase if you have enough gold")
        print(make_dictionary_table(self.shopDict))

    def handleAction(self, command, args=""):
        if command == "main":
            self.game.change_scene("main")
        if command == "buy":
            pass


class Adventure(Scene):
    def __init__(self, game):
        super().__init__(game)

    def display(self):
        print(colored("---Adventure---", "yellow"))

    def handleAction(self, command, args=""):
        pass





# Action Classes

class Action(ABC):

    @abstractmethod
    def execute(self, command, args=""):
        pass
