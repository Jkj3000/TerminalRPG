from beautifultable import BeautifulTable
from termcolor import colored

def makeDictionaryTable(dictionary):
    table = BeautifulTable()
    table.columns.header = ["Stat", "Value"]
    for key, value in dictionary.items():
        table.rows.append([key, colored(value, "red")])
    return table