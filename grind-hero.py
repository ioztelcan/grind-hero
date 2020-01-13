#!venv/bin/python3
import signal, sys
import chars, config, util, objects, tui
import time
import argparse
import yaml
import curses

def encounter(hero):
    monster = chars.Mob(hero.lvl)
    tui.log("Executing a(n) {} {}!".format(monster.adjective, monster.name))
    tui.run_progress_bar(config.TURN_SPEED / util.modifier(hero.lvl, monster.lvl))
    
    #tui.log("Attacking the {} {}.".format(monster.adjective, monster.name))
    #tui.run_progress_bar(config.TURN_SPEED)
    
    # Disable complex fight mechanics for now
    #while (monster.hp > 0):
        #print(".".format(monster.hp), end="", flush=True)
        #dmg_given = int(hero.attack * util.modifier(hero.lvl, monster.lvl))
        #dmg_taken = int(max(1, dmg_given - monster.defense * util.modifier(hero.lvl, monster.lvl)))
        #monster.hp = monster.hp - dmg_taken
        #time.sleep(config.TURN_SPEED)
    
    #tui.log("Defeated the {} {}!".format(monster.adjective, monster.name))
    #tui.log("Earned {} experience.".format(monster.exp))
    hero.exp = monster.exp + hero.exp
    if (hero.exp >= hero.exp_next_lvl):
        tui.log("Level up! {} -> {}".format(hero.lvl, hero.next_lvl))
        hero.level_up()
    
    tui.log("Looting corpse.")
    tui.run_progress_bar(config.TURN_SPEED / 3)
    hero.shitcoins = monster.shitcoins + hero.shitcoins
    #print("{} shitcoins".format(monster.shitcoins), end="", flush=True)
    for i in range(monster.loot_amount):
        loot = objects.Item(monster.lvl)
        hero.inventory.append(loot)
        #print(", {} {}".format(loot.adjective, loot.name), end="", flush=True)
    #print("")

def go_to_dungeon(hero):
    tui.log("Going to a dungeon.")
    tui.run_progress_bar(config.TURN_SPEED)
    tui.log("Looking for monsters to pick a fight with.")
    tui.run_progress_bar(config.TURN_SPEED)
    while len(hero.inventory) < 20: # Possibly change inventory size with upgrades?
        time.sleep(config.TURN_SPEED)
        encounter(hero)

def go_to_town(hero):
    tui.log("Going to town to sell the loot.")
    tui.run_progress_bar(config.TURN_SPEED)
    for item in hero.inventory:
        tui.log("Selling {} {}.".format(item.adjective, item.name))
        hero.shitcoins = hero.shitcoins + item.value
        tui.run_progress_bar(config.TURN_SPEED / 3)
    hero.inventory = []

def start(hero):
    while True:
        go_to_dungeon(hero)
        go_to_town(hero)

def bootstrap():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--char", required=False, help="Character file that was saved before, if not provided, new one will be generated.")
    parser.add_argument("-t", "--tui", type=bool, required=False, help="Launches text user interface if given.")
    args = parser.parse_args()
    if args.char == None:
        print("No saved character provided, generating a new hero...")
        name = input("Please provide a new name for your \"hero\": ")
        hero = chars.Hero()
        hero.generate_new(name)
    else:
        print("Loading hero...")
        time.sleep(0.5)
        hero = chars.Hero()
        hero.load_info(args.char)

    if args.tui == True:
        scr = tui.init()
        tui.update_stats_panel(hero)

    def sigint_handler(sig, frame):
        tui.log("Saving info, exiting game.")
        time.sleep(0.5)
        hero.save_info()
        scr.die()
        sys.exit(0)
        
    # Register SIGINT handler for graceful termination.
    signal.signal(signal.SIGINT, sigint_handler)
    return hero

if __name__ == "__main__":
    hero = bootstrap()
    start(hero)
