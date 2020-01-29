#!/usr/bin/env python3
import chars, config, util, objects, tui
import signal, sys
import time
import argparse
import yaml
import curses
import logging

def encounter(hero):
    monster = chars.Mob(hero.lvl)
    util.log("Executing a(n) {} {}!".format(monster.adjective, monster.name))
    util.debug_log("lvl:{} exp:{} sc:{}".format(monster.lvl, monster.exp, monster.shitcoins))
    tui.run_progress_bar(config.TURN_SPEED / util.modifier(hero.lvl, monster.lvl))
    
    hero.exp = int(monster.exp + hero.exp)
    util.debug_log("Earned {} experience.".format(monster.exp))
    if (hero.exp >= hero.exp_next_lvl):
        util.log("Level up! {} -> {}".format(hero.lvl, hero.next_lvl))
        hero.level_up()
    tui.update_stats_panel(hero)
    
    util.log("Looting corpse.")
    tui.run_progress_bar(config.TURN_SPEED / 3)
    hero.shitcoins = monster.shitcoins + hero.shitcoins
    tui.update_inventory_panel(hero)
    util.debug_log("- {} shitcoins".format(monster.shitcoins))
    for i in range(monster.loot_amount):
        loot = objects.Item(monster.lvl)
        hero.inventory.append(loot)
        tui.update_inventory_panel(hero)
        util.debug_log("- {} {} lvl:{} val:{}".format(loot.adjective, loot.name, loot.lvl, loot.value))


def go_to_dungeon(hero):
    util.log("Going to a dungeon.")
    tui.run_progress_bar(config.TURN_SPEED)
    util.log("Looking for monsters to pick a fight with.")
    tui.run_progress_bar(config.TURN_SPEED)
    while len(hero.inventory) < 20: # Possibly change inventory size with upgrades?
        time.sleep(config.TURN_SPEED)
        encounter(hero)

def go_to_town(hero):
    util.log("Going to town to sell the loot.")
    tui.run_progress_bar(config.TURN_SPEED)
    temp_inv = hero.inventory.copy()
    for item in temp_inv:
        util.log("Selling {} {}.".format(item.adjective, item.name))
        hero.shitcoins = hero.shitcoins + item.value
        hero.inventory.remove(item)
        tui.run_progress_bar(config.TURN_SPEED / 3)
        tui.update_inventory_panel(hero)
    #hero.inventory = []

def start(hero):
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
        time.sleep(0.5)
        hero = chars.Hero()
        hero.load_info(args.char)
        
    logfile = config.LOGS_LOCATION + hero.name + '.log'
    logging.basicConfig(filename=logfile,level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s')
    scr = tui.init()
    tui.update_stats_panel(hero)
    tui.update_inventory_panel(hero)

    def sigint_handler(sig, frame):
        util.log("Saving info, exiting game.")
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
