from beautifultable import BeautifulTable
from termcolor import colored
import os
from abc import ABC, abstractmethod


# Support Functions
def make_dictionary_table(data, headersList):
    table = BeautifulTable()
    table.columns.header = headersList

    if type(data) == dict:
        if len(data) == 0:
            # Add empty row for visibility
            table.rows.append([""] * len(headersList))
        else:
            for key, value in data.items():
                table.rows.append([key, colored(value, "red")])
    elif type(data) == list:
        if len(data) == 0:
            # create empty row matching header length
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

                # If headers expect 4 columns include all 4
                if len(headersList) == 4:
                    table.rows.append([index, colored(nameOfItem, "blue"), colored(str(priceOfItem), "green"), colored(buffs_str, "cyan")])
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

class Rat(Creature):
    def __init__(self):
        # Light, weak enemy good for early encounters
        stats = {
            "HP": 6,
            "DMG": 2,
            "DEF": 0,
            "Gold": 2
        }
        super().__init__(stats, inventoryList=[])
        self.name = "Rat"

    def receive_damage(self, amount):
        # Damage reduced by DEF, minimum 0
        effective = max(amount - self.stats.get("DEF", 0), 0)
        self.stats["HP"] = max(0, self.stats["HP"] - effective)
        return effective

    @property
    def is_alive(self):
        return self.stats.get("HP", 0) > 0

    def brief(self):
        return f"{self.name} (HP:{self.stats['HP']} DMG:{self.stats['DMG']} DEF:{self.stats['DEF']})"


class Goblin(Creature):
    def __init__(self):
        stats = {
            "HP": 18,
            "DMG": 5,
            "DEF": 1,
            "Gold": 6
        }
        super().__init__(stats, inventoryList=[])
        self.name = "Goblin"

    def receive_damage(self, amount):
        effective = max(amount - self.stats.get("DEF", 0), 0)
        self.stats["HP"] = max(0, self.stats["HP"] - effective)
        return effective

    @property
    def is_alive(self):
        return self.stats.get("HP", 0) > 0

    def brief(self):
        return f"{self.name} (HP:{self.stats['HP']} DMG:{self.stats['DMG']} DEF:{self.stats['DEF']})"





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
        print("Commands: adventure, inventory, shop, quit")
        print(make_dictionary_table(self.game.player.inventoryListOfDict, ["Index", "Name", "Price", "Buffs"]))
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
        self.current_enemy = None
        self.player_defending = False
        self.enemy_defending = False
        self.battle_active = False

    def display(self):
        if self.battle_active and self.current_enemy:
            # Battle screen
            print(colored("---BATTLE---", "red"))
            print(f"Player: HP {colored(str(self.game.player.stats.get('HP', 0)), 'green')} | DMG {self.game.player.stats.get('DMG', 1)} | DEF {self.game.player.stats.get('DEF', 0)}")
            print(f"Enemy ({self.current_enemy.name}): HP {colored(str(self.current_enemy.stats.get('HP', 0)), 'red')} | DMG {self.current_enemy.stats.get('DMG', 1)} | DEF {self.current_enemy.stats.get('DEF', 0)}")
            print("\nCommands: hit, defend")
        else:
            # Main adventure screen
            print(colored("---Adventure---", "yellow"))
            print("Commands: main, battle <rat|goblin>, quit")

    def handleAction(self, command, args=""):
        if not self.battle_active:
            # Outside of battle
            if command == "main":
                self.game.enter_scene("main")
            elif command == "battle":
                self.start_battle(args.strip().lower())
        else:
            # During battle
            if command == "hit":
                self.player_action_hit()
            elif command == "defend":
                self.player_action_defend()
            else:
                print(colored("Invalid action! Use 'hit' or 'defend'", "red"))
                input("Press Enter to continue...")

    def start_battle(self, enemy_type):
        # Initialize a battle with the specified enemy
        if enemy_type == "rat":
            self.current_enemy = Rat()
        elif enemy_type == "goblin":
            self.current_enemy = Goblin()
        else:
            print(colored("Usage: battle <rat|goblin>", "red"))
            input("Press Enter to continue...")
            return

        self.battle_active = True
        self.player_defending = False
        self.enemy_defending = False
        print(colored(f"A wild {self.current_enemy.name} appears!", "yellow"))
        print(f"{self.current_enemy.brief()}")
        input("Press Enter to start the battle...")

    def player_action_hit(self):
        # Player chooses to hit
        player = self.game.player
        enemy = self.current_enemy

        # Player attacks
        player_dmg = player.stats.get("DMG", 1)
        # Enemy DEF reduces damage; if defending, DEF is doubled
        enemy_def = enemy.stats.get("DEF", 0)
        if self.enemy_defending:
            enemy_def *= 2
        dealt = max(player_dmg - enemy_def, 1)  # minimum 1 damage
        enemy.stats["HP"] = max(0, enemy.stats["HP"] - dealt)
        print(colored(f"\nYou attack the {enemy.name} for {dealt} damage!", "cyan"))
        print(f"Enemy HP: {enemy.stats['HP']}/{enemy.stats.get('HP', 0) + dealt}")

        self.player_defending = False
        self.enemy_defending = False

        # Check if enemy is dead
        if enemy.stats["HP"] <= 0:
            self.end_battle_victory()
            return

        # Enemy turn
        self.enemy_turn()

    def player_action_defend(self):
        # Player chooses to defend
        self.player_defending = True
        print(colored("\nYou take a defensive stance!", "yellow"))
        print("Your DEF is doubled this turn.")

        self.enemy_defending = False

        # Enemy turn
        self.enemy_turn()

    def enemy_turn(self):
        # Enemy AI and attack
        player = self.game.player
        enemy = self.current_enemy

        # Simple AI: enemy hits or defends randomly (70% hit, 30% defend)
        import random
        if random.random() < 0.7:
            # Enemy attacks
            enemy_dmg = enemy.stats.get("DMG", 1)
            player_def = player.stats.get("DEF", 0)
            if self.player_defending:
                player_def *= 2
            dealt = max(enemy_dmg - player_def, 1)
            player.stats["HP"] = max(0, player.stats["HP"] - dealt)
            print(colored(f"The {enemy.name} attacks you for {dealt} damage!", "red"))
            print(f"Your HP: {player.stats['HP']}")
            self.enemy_defending = False
        else:
            # Enemy defends
            print(colored(f"The {enemy.name} takes a defensive stance!", "magenta"))
            self.enemy_defending = True

        # Check if player is dead
        if player.stats["HP"] <= 0:
            self.end_battle_defeat()
            return

        input("Press Enter for your next action...")

    def end_battle_victory(self):
        # Handle battle victory
        player = self.game.player
        enemy = self.current_enemy
        gold_reward = enemy.stats.get("Gold", 0)

        print(colored(f"\n{'='*40}", "green"))
        print(colored(f"You defeated the {enemy.name}!", "green"))
        print(colored(f"You gained {gold_reward} gold!", "yellow"))
        print(colored(f"{'='*40}\n", "green"))

        player.stats["Gold"] = player.stats.get("Gold", 0) + gold_reward
        self.battle_active = False
        self.current_enemy = None
        input("Press Enter to return to adventure...")

    def end_battle_defeat(self):
        # Handle battle defeat
        print(colored(f"\n{'=' * 40}", "red"))
        print(colored("You have been defeated...", "red"))
        print(colored(f"{'=' * 40}\n", "red"))

        # Delete save file on defeat
        if os.path.exists("savegame.json"):
            os.remove("savegame.json")
            print(colored("Your save file has been deleted.", "red"))

        self.battle_active = False
        self.current_enemy = None
        input("Press Enter to return to main menu...")
        self.game.enter_scene("main")

# Action Classes

class Action(ABC):

    @abstractmethod
    def execute(self, command, args=""):
        pass