from beautifultable import BeautifulTable
from termcolor import colored
import os
from abc import ABC, abstractmethod


# Support Functions
def makeDictionaryTable(dictionary):
    table = BeautifulTable()
    table.columns.header = ["Stat", "Value"]
    for key, value in dictionary.items():
        table.rows.append([key, colored(value, "red")])
    return table

def clearWindow():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def compareStats(stat1, stat2):
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
        print(makeDictionaryTable(self.game.player.stats))

    def handleAction(self, command, args=""):
        if command == "adventure":
            self.game.enter_scene("adventure")
        if command == "shop":
            self.game.enter_scene("shop")
        if command == "city":
            self.game.enter_scene("city")
        if command == "stats":
            makeDictionaryTable(self.game.player.stats)

class Shop(Scene):
    def __init__(self, game):
        self.shopDict = {}
        super().__init__(game)

    def display(self):
        print(colored("---Shop---", "yellow"))
        print("How to purchase:\nType 1-n to purchase if you have enough gold")
        print(makeDictionaryTable(self.shopDict))

    def handleAction(self, command, args=""):
        pass

class Adventure(Scene):
    def __init__(self, game):
        super().__init__(game)

    def display(self):
        print(colored("---Adventure---", "yellow"))

    def handleAction(self, command, args=""):
        pass

# Action Classes