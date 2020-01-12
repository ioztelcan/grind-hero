import tui


def modifier(player_lvl, mob_lvl):
    diff = (mob_lvl - player_lvl)/10
    return 1 + diff

def log(string):
    if tui_enabled == True:
        window.prnt(string)
    else:
        print(string)

        
