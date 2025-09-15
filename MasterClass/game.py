
import random


def roll_dice(sides=6):
    """ Rolls dice based on parameter, default to 6 sided dice """
    return random.randint(1, sides)


def crit(dmg):
    """ if dice roll was 6 then crits the damage )*2 """
    return dmg * 2 if roll_dice(6) == 6 else dmg


def attack(player, monster):
    damage = roll_dice()
    final_damage = crit(damage)
    if final_damage > damage:
        print(f"💥 Critical hit! {player} smashes {monster} for {final_damage} damage!")
    else:
        print(f"{player} hits {monster} for {damage} damage.")
    return final_damage


def heal(player):
    amount = roll_dice(8)
    print(f"{player} drinks a potion and restores {amount} HP!")
    return amount


def battle(player, monster, health=20):
    print(f"\n⚔️ A wild {monster} appears with {health} HP!\n")
    player_health = 30

    while health > 0 and player_health > 0:
        action = input("Choose action: (a)ttack or (h)eal: ").lower()

        if action == "a":
            dmg = attack(player, monster)
            health -= dmg
            print(f"{monster} has {max(health,0)} HP left.\n")
        elif action == "h":
            player_health += heal(player)
            print(f"{player} now has {player_health} HP.\n")
        else:
            print("Invalid action! You lose your turn.")

        # Monster attacks back if still alive
        if health > 0:
            monster_dmg = roll_dice(6)
            player_health -= monster_dmg
            print(f"{monster} hits {player} for {monster_dmg} damage! {player} has {max(player_health,0)} HP left.\n")

    # End of battle
    if player_health <= 0:
        print(f"💀 {player} has been defeated by {monster}...")
        return False
    else:
        print(f"🏆 {monster} is defeated!")
        return True


def game():
    print("Welcome to MONSTER BATTLE!")
    player = input("Enter your hero's name: ")

    monsters = ["Goblin", "Orc", "Dragon"]
    for m in monsters:
        survived = battle(player, m, health=roll_dice(20) + 10)
        if not survived:
            print("Game Over.")
            break
    else:
        print(f"🎉 {player} defeated all the monsters! You win!")


game()
