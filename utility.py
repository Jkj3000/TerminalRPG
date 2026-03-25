from beautifultable import BeautifulTable
from termcolor import colored
import os

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






