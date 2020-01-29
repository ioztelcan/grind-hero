import tui
import logging
import config


def modifier(player_lvl, mob_lvl):
    diff = (mob_lvl - player_lvl)/10
    return 1 + diff

def log(string):
    tui.log(string)
    logging.info(string)

def debug_log(string):
    logging.debug(string)
        
