#!./venv/bin/python3
import signal, sys
import chars, config, util, tui
import time
import argparse
import yaml
import curses

def encounter(hero):
    monster = chars.Mob(hero.lvl)
    print("Encountered a(n) {} {}!".format(monster.adjective, monster.name))
    time.sleep(0.5)
    print("Attacking the {} {}...".format(monster.adjective, monster.name))
    
    # fight fight fight
    while (monster.hp > 0):
        print(".".format(monster.hp), end="", flush=True)
        dmg_given = int(hero.attack * chars.util(hero.lvl, monster.lvl))
        dmg_taken = int(max(1, dmg_given - monster.defense * chars.util(hero.lvl, monster.lvl)))
        monster.hp = monster.hp - dmg_taken
        time.sleep(config.TURN_SPEED)
    
    pbar.close()
    print("\nDefeated the {} {}!".format(monster.adjective, monster.name))
    print("Earned {} experience, looted {} shitcoin(s).".format(monster.exp, monster.shitcoins))
    hero.exp = monster.exp + hero.exp
    hero.shitcoins = monster.shitcoins + hero.shitcoins

def go_to_dungeon(hero):
    print("Going to a dungeon...")
    time.sleep(1)
    print("Looking for monsters to pick a fight with.")
    time.sleep(1)
    while True: # replace with inventory full
        time.sleep(config.TURN_SPEED)
        encounter(hero)
        if (hero.exp >= hero.next_lvl * 1000):
            print("Level up! {} -> {}".format(hero.lvl, hero.next_lvl))
            hero.lvl = hero.next_lvl
            hero.next_lvl = hero.next_lvl + 1
            hero.print_stats()

def start(hero):
    print ("Idle game start!") 
    go_to_dungeon(hero)

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
        print("Saving info, exiting game.")
        hero.save_info()
        sys.exit(0)
        
    # Register SIGINT handler for graceful termination.
    signal.signal(signal.SIGINT, sigint_handler)

    hero.print_stats()
    return hero

if __name__ == "__main__":
    hero = bootstrap()
    start(hero)
