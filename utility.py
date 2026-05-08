from beautifultable import BeautifulTable
from termcolor import colored
import os
from abc import ABC, abstractmethod
##TODO: Add table gen for lists
##TODO: Add shop scene
    ##TODO: Add display of items
    ##TODO: Add purchace
##TODO: add player inventory

# Support Functions
def make_dictionary_table(data, headersList):
    if type(data) == dict:
        table = BeautifulTable()
        table.columns.header = headersList
        for key, value in data.items():
            table.rows.append([key, colored(value, "red")])
        return table
    elif type(data) == list:
        table = BeautifulTable()
        table.columns.header = headersList
        index = 0
        for dictOfItem in data:
            nameOfItem = ""
            priceOfItem = ""
            for key, value in dictOfItem.items():
                nameOfItem = key
                priceOfItem = value
            table.rows.append([index, colored(nameOfItem, "blue"), colored(priceOfItem, "green")])
            index += 1
        return table

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
    def __init__(self, statsDict, inventoryList=[]):
        self.stats = statsDict
        self.inventoryListOfDict = inventoryList

    def accesStat(self, statKey):
        for key in self.stats:
            if statKey in key:
                return self.stats[key]

    def accesInventoryDict(self, index):
        return self.inventoryListOfDict[index]

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
        print("Commands: adventure, inventory, city, quit")
        print(make_dictionary_table(self.game.player.stats, ["Stat", "Value"]))

    def handleAction(self, command, args=""):
        if command == "adventure":
            self.game.enter_scene("adventure")
        if command == "shop":
            self.game.enter_scene("shop")
        if command == "city":
            self.game.enter_scene("city")
        if command == "stats":
            make_dictionary_table(self.game.player.stats, ["Stat", "Value"])
        if command == "inventory":
            make_dictionary_table(self.game.player.inventoryListOfDict)

class Shop(Scene):
    def __init__(self, game):
        self.shopList = [
        {"Basic Sword": 10},
        {"Medium Sword": 100},
        {"Epic Sword": 500},
        {"Legendary Sword": 5000},
        {"Basic Shield": 100},
        {"Medium Shield": 500},
        {"Epic Shield": 5000},
        {"Legendary Shield": 8000}
    ]
        super().__init__(game)

    def display(self):
        # Text
        print(colored("---Shop---", "yellow"))
        print("Commands: main, buy 1-n, inventory")
        print("How to purchase:\nType 1-n to purchase if you have enough gold")
        print(make_dictionary_table(self.shopList, ["Index", "Item", "Price"]))
        print(make_dictionary_table(self.game.player.inventoryListOfDict, ["Index", "Name", "Description"]))

    def handleAction(self, command, args=""):
        if command == "main":
            self.game.enter_scene("main")
        if command == "buy":
            pass


class Adventure(Scene):
    def __init__(self, game):
        super().__init__(game)

    def display(self):
        print(colored("---Adventure---", "yellow"))
        print("Commands: main, battle, quit")

    def handleAction(self, command, args=""):
        if command == "main":
            self.game.enter_scene("main")


# Action Classes

class Action(ABC):

    @abstractmethod
    def execute(self, command, args=""):
        pass
