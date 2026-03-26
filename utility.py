from beautifultable import BeautifulTable
from samba.samba3.mdscli import conn
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
    def __init__(self, statsDict):
        self.stats = statsDict

    def accesStat(self, statKey):
        for key in self.stats:
            if statKey in key:
                return self.stats[key]

class Player(Creature):
    def __init__(self, statsDict, inventoryList=[]):
        self.inventoryList = inventoryList
        super().__init__(statsDict)

    def accesInventory(self, index):
        return self.inventoryList[index]

class Enemy(Creature):
    def __init__(self, statsDict, lootTable):
        self.lootTable = lootTable
        super().__init__(statsDict)

    def accesLootDict(self, index):
        return self.lootTable[index]



# Scene classes
class Scene(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def handleCommand(self, command):
        pass

class MainScreen(Scene):
    def display(self):
        print(colored("---Main Screen---", "yellow"))
        print("Commands: adventure, shop, city, quit")
        print(makeDictionaryTable(player.a))

    def handleCommand(self, command):
        if command == "adventure":
            pass
        elif command == "shop":
            pass
        elif command == "city":
            pass

class Shop(Scene):
    def __init__(self, shopDict):
        self.shopDict = shopDict
        super().__init__()

    def display(self):
        print(colored("---Shop---", "yellow"))
        print("How to purchase:\nType 1-n to purchase if you have enough gold")
        print(makeDictionaryTable(self.shopDict))

    def handleCommand(self, command):
        pass

class City(Scene):
    def display(self):
        print(colored("---City---", "yellow"))

    def handleCommand(self, command):
        pass


# Action Classes
def