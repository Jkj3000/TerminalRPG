    #TODO: Make a Player and Enemy child class with loot for enemy and inventory for player
#TODO: Make a function that starts a fight

import utility
from utility import Player

attributes = {
    "HP": 100,
    "Mana": 500,
    "Dmg": 5,
    "Defense": 5,
}

player = Player(attributes)

print(player.accesStat("HP"))

