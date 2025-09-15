
import random


class Die:
    '''
    A class representing a die with a specified number of sides.

    Attributes:
        sides (int): The number of sides on the die.

    Methods:
        roll() -> int: Simulates rolling the die and returns a random integer
                       between 1 and the number of sides inclusive.
    '''
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


attack_damage = Die(20)


# def roll_dice():
#     print("Rolling the dice ...")


# def attack(player, monster) -> str:
#     '''
#     Simulate an attack from player to monster.

#     Parameters:
#         player (str): The name of the player.
#         monster (str): The name of the monster.

#     Returns:
#         str: A message indicating the attack action.
#     '''
#     return f"{player} attacks {monster}"


# def cast_spell(player, spell):
#     print(f"{player} casts {spell}")


# print(attack("Hero", "Dragon"))
# print(attack_damage.roll())

def inventory(*args):
    for item in args:
        print(item)


inventory("Sword", "Shield", "Potion")


crit = lambda dmg: dmg * 2


print(crit(attack_damage.roll()))
