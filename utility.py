from beautifultable import BeautifulTable
from termcolor import colored
import os
from abc import ABC, abstractmethod
##TODO: Add shop scene
    ##TODO: Add purchace
##TODO: add player inventory

# Support Functions
def make_dictionary_table(data, headersList):
    table = BeautifulTable()
    table.columns.header = headersList

    if type(data) == dict:
        if len(data) == 0:
            # Add empty row for visibility
            table.rows.append(["", ""])
        else:
            for key, value in data.items():
                table.rows.append([key, colored(value, "red")])
    elif type(data) == list:
        if len(data) == 0:
            # create empty row matching a 3- or 4-column layout
            # use length of headers to decide columns
            cols = len(headersList)
            table.rows.append([""] * cols)
        else:
            index = 0
            for dictOfItem in data:
                nameOfItem = ""
                priceOfItem = ""
                buffs_str = ""
                for key, value in dictOfItem.items():
                    nameOfItem = key
                    # value can be old-format price (int) or new-format dict
                    if isinstance(value, dict):
                        priceOfItem = value.get("price", "")
                        buffs = value.get("buffs", {})
                        if buffs:
                            buffs_str = ", ".join([f"{k}+{v}" for k, v in buffs.items()])
                    else:
                        priceOfItem = value

                # If headers expect 4 columns (Index, Name, Price, Buffs) include buffs column
                if len(headersList) >= 4:
                    table.rows.append([index, colored(nameOfItem, "blue"), colored(str(priceOfItem), "green"), buffs_str])
                else:
                    table.rows.append([index, colored(nameOfItem, "blue"), colored(str(priceOfItem), "green")])
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

    # New: apply buffs from an item (item in the same format used in shop/inventory)
    def apply_buffs_from_item(self, item):
        """
        item is a dict with single key: name -> value
        value may be int (old format) or dict with 'price' and optional 'buffs'
        """
        try:
            info = list(item.values())[0]
        except Exception:
            return

        if isinstance(info, dict):
            buffs = info.get("buffs", {})
            for stat, amount in buffs.items():
                # Ensure stat key exists; if not, create it
                if stat in self.stats:
                    self.stats[stat] += amount
                else:
                    self.stats[stat] = amount

    def remove_buffs_from_item(self, item):
        try:
            info = list(item.values())[0]
        except Exception:
            return

        if isinstance(info, dict):
            buffs = info.get("buffs", {})
            for stat, amount in buffs.items():
                if stat in self.stats:
                    self.stats[stat] -= amount

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
        print(make_dictionary_table(self.game.player.inventoryListOfDict, ["Index", "Name", "Price", "Buffs"]))

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
            print(make_dictionary_table(self.game.player.inventoryListOfDict, ["Index", "Name", "Value"]))
            input("Press Enter to continue...")

class Shop(Scene):
    def __init__(self, game):
        self.shopList = [
            {"Basic Sword": {"price": 10, "buffs": {"DMG": 2}}},
            {"Medium Sword": {"price": 100, "buffs": {"DMG": 5}}},
            {"Epic Sword": {"price": 500, "buffs": {"DMG": 15}}},
            {"Legendary Sword": {"price": 5000, "buffs": {"DMG": 50}}},
            {"Basic Shield": {"price": 100, "buffs": {"DEF": 2}}},
            {"Medium Shield": {"price": 500, "buffs": {"DEF": 8}}},
            {"Epic Shield": {"price": 5000, "buffs": {"DEF": 25}}},
            {"Legendary Shield": {"price": 8000, "buffs": {"DEF": 80}}}
        ]
        super().__init__(game)

    def display(self):
        print(colored("---Shop---", "yellow"))
        print(f"Gold: {colored(str(self.game.player.accesStat('Gold')), 'yellow')}")
        print("Commands: main, buy 0-n, inventory")
        print("How to purchase:\nType 'buy n' where n is the item index")
        print(make_dictionary_table(self.shopList, ["Index", "Item", "Price", "Buffs"]))
        print(make_dictionary_table(self.game.player.inventoryListOfDict, ["Index", "Name", "Price", "Buffs"]))

    def handleAction(self, command, args=""):
        if command == "main":
            self.game.enter_scene("main")
        if command == "buy":
            if args == "":
                print("Usage: buy <index>")
                return

            try:
                index = int(args)
                if 0 <= index < len(self.shopList):
                    item = self.shopList[index]
                    itemName = list(item.keys())[0]
                    itemPrice = item[itemName]
                    itemInfo = item[itemName]
                    if isinstance(itemInfo, dict):
                        itemPrice = itemInfo.get("price", 0)
                    else:
                        itemPrice = itemInfo
                    playerGold = self.game.player.accesStat("Gold")

                    if playerGold >= itemPrice:
                        # Purchase successful
                        self.game.player.inventoryListOfDict.append(item)
                        # Apply buffs if present
                        self.game.player.apply_buffs_from_item(item)

                        # Deduct gold
                        self.game.player.stats["Gold"] -= itemPrice
                        self.shopList.pop(index)
                        print(colored(f"Purchased {itemName} for {itemPrice} gold!", "green"))
                        input("Press Enter to continue...")
                    else:
                        print(colored(f"Not enough gold! Need {itemPrice}, have {playerGold}", "red"))
                        input("Press Enter to continue...")
                else:
                    print(colored("Invalid item index!", "red"))
                    input("Press Enter to continue...")
            except ValueError:
                print(colored("Invalid command format. Use: buy <number>", "red"))
                input("Press Enter to continue...")


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
