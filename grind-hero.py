#!./venv/bin/python3
import signal, sys
import chars, config, util, objects, tui
import time
import argparse
import yaml
import curses

# Group level up adjustments here.
def level_up(hero):
    print("Level up! {} -> {}".format(hero.lvl, hero.next_lvl))
    hero.lvl = hero.next_lvl
    hero.next_lvl = hero.next_lvl + 1
    hero.exp_next_lvl = hero.exp + hero.next_lvl * 1000
    hero.print_stats()       

def encounter(hero):
    monster = chars.Mob(hero.lvl)
    print("Encountered a(n) {} {}!".format(monster.adjective, monster.name))
    time.sleep(0.5)
    print("Attacking the {} {}.".format(monster.adjective, monster.name))
    
    # fight fight fight
    while (monster.hp > 0):
        print(".".format(monster.hp), end="", flush=True)
        dmg_given = int(hero.attack * util.modifier(hero.lvl, monster.lvl))
        dmg_taken = int(max(1, dmg_given - monster.defense * util.modifier(hero.lvl, monster.lvl)))
        monster.hp = monster.hp - dmg_taken
        time.sleep(config.TURN_SPEED)
    
    print("\nDefeated the {} {}!".format(monster.adjective, monster.name))
    print("Earned {} experience.".format(monster.exp))
    hero.exp = monster.exp + hero.exp
    if (hero.exp >= hero.exp_next_lvl):
        level_up(hero)
    print("Looting corpse.")    
    hero.shitcoins = monster.shitcoins + hero.shitcoins
    print("{} shitcoins".format(monster.shitcoins), end="", flush=True)
    for i in range(monster.loot_amount):
        loot = objects.Item(monster.lvl)
        hero.inventory.append(loot)
        print(", {} {}".format(loot.adjective, loot.name), end="", flush=True)
    print("")

def go_to_dungeon(hero):
    print("Going to a dungeon.")
    time.sleep(1)
    print("Looking for monsters to pick a fight with.")
    time.sleep(1)
    while len(hero.inventory) < 20: # Possibly change inventory size with upgrades?
        time.sleep(config.TURN_SPEED)
        encounter(hero)

def go_to_town(hero):
    print("Going to town to sell the loot.")
    for item in hero.inventory:
        print("Selling {} {}.".format(item.adjective, item.name))
        hero.shitcoins = hero.shitcoins + item.value
        time.sleep(0.1)
    hero.inventory = []

def start(hero):
    print ("Idle game start!") 
    while True:
        go_to_dungeon(hero)
        go_to_town(hero)

def bootstrap():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--char", required=False, help="Character file that was saved before, if not provided, new one will be generated.")
    args = parser.parse_args()
    if args.char == None:
        print("No saved character provided, generating a new hero...")
        name = input("Please provide a new name for your \"hero\": ")
        hero = chars.Hero()
        hero.generate_new(name)
    else:
        print("Loading hero...")
        hero = chars.Hero()
        hero.load_info(args.char)

    def sigint_handler(sig, frame):
        print("\nSaving info, exiting game.")
        hero.save_info()
        # de-init tui as well.
        sys.exit(0)
        
    # Register SIGINT handler for graceful termination.
    signal.signal(signal.SIGINT, sigint_handler)

    hero.print_stats()
    return hero

if __name__ == "__main__":
    hero = bootstrap()
    start(hero)
