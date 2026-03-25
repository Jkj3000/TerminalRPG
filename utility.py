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

class Creature:
    def __init__(self, statsDict):
        self.stats = statsDict

    def accesStat(self, statKey):
        for key in self.stats:
            if statKey in key:
                return self.stats[key]


