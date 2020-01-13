import curses
import os, sys
import time

scr = None
stats_panel = None
equipped_panel = None
inventory_panel = None
log_panel = None
progress_panel = None

class Screen():

    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.clear()
        self.stdscr.refresh()

        self.height, self.width = self.stdscr.getmaxyx()
        self.start_x = 0
        self.start_y = 0
        self.quarter_w = int(self.width // 4)
        self.half_w = int(self.width // 2)
        self.quarter_h = int(self.height // 4)
        self.half_h = int(self.height // 2)
        self.refresh()

    def write(self, row, col, string):
        self.stdscr.addstr(row, col, string)
        self.refresh()

    def die(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def refresh(self):
        self.stdscr.refresh()
    
    def clear(self):
        self.stdscr.refresh()

class Panel():

    def __init__ (self, rows, cols, start_row, start_col, title):
        self.start_row = 1
        self.start_col = 1
        self.rows = rows
        self.cols = cols
        self.view = curses.newwin(rows, cols, start_row, start_col)
        self.view.border()
        self.title = title
        self._update_title()

    def clear(self):
        self.view.clear()
        self.view.border()
        self._update_title()
        self.refresh()

    def refresh(self):
        self.view.refresh()

    def write(self, row, col, string):
        self.view.addstr(row, col, string)
        self.refresh()

    def _update_title(self):
        self.view.attron(curses.color_pair(1))
        self.view.addstr(self.start_row - 1, self.start_col, self.title)
        self.view.attroff(curses.color_pair(1))
        self.refresh()


def init():
    global scr
    scr = Screen()
    
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.curs_set(False)

    scr.stdscr.attron(curses.color_pair(3))
    scr.write(scr.height - 1, 0, "GRIND HERO v0.0.1 - Welcome to the grind yo.")
    # Trick to fill whitespace for the rest of the bar.
    #stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    scr.stdscr.attroff(curses.color_pair(3))
    
    global stats_panel
    stats_panel = Panel(scr.height - 7, scr.quarter_w, scr.start_y, scr.start_x, "STATS")

    global equipped_panel
    equipped_panel = Panel(scr.height - 7, scr.quarter_w, scr.start_y, scr.start_x + scr.quarter_w, "EQUIPPED")

    global inventory_panel
    inventory_panel = Panel(scr.height - 1, scr.half_w, scr.start_y, scr.start_x + scr.half_w, "INVENTORY")
    
    global log_panel
    log_panel = Panel(3, scr.half_w, scr.height - 7, scr.start_x, "")
   
    global progress_panel
    progress_panel = Panel(3, scr.half_w, scr.height - 4, scr.start_x, "")
    
    return scr

def update_stats_panel(hero):
    #Write line by line like a caveman because why not
    stats_panel.write(stats_panel.start_row,stats_panel.start_col,"{}  |  Lvl {}".format(hero.name, hero.lvl))
    stats_panel.write(stats_panel.start_row + 1,stats_panel.start_col,"-" * (stats_panel.cols - 2))
    stats_panel.write(stats_panel.start_row + 2,stats_panel.start_col,"HP: {}".format(hero.hp))
    stats_panel.write(stats_panel.start_row + 3,stats_panel.start_col,"ATT: {}".format(hero.attack))
    stats_panel.write(stats_panel.start_row + 4,stats_panel.start_col,"DEF: {}".format(hero.defense))
    stats_panel.write(stats_panel.start_row + 5,stats_panel.start_col,"NEXT_LVL: {}/{} ".format(hero.exp, hero.exp_next_lvl))
   
def update_inventory_panel(hero):
    inventory_panel.clear()
    inventory_panel.write(inventory_panel.start_row,inventory_panel.start_col,"{} shitcoins".format(hero.shitcoins))
    inventory_panel.write(inventory_panel.start_row + 1,inventory_panel.start_col,"-" * (inventory_panel.cols - 2))
    i = 1
    for item in hero.inventory:
        inventory_panel.write(inventory_panel.start_row + 1 + i,inventory_panel.start_col,"{} {}".format(item.adjective, item.name))
        i = i + 1


def log(string):
    # Write to a log file.
    # Write to log panel.
    log_panel.clear()
    log_panel.write(log_panel.start_row, log_panel.start_col, string)

def run_progress_bar(speed):
    progress_panel.clear()
    i = 0
    for i in range(progress_panel.cols - 2):
        progress_panel.view.attron(curses.color_pair(3))
        progress_panel.write(progress_panel.start_row, progress_panel.start_col + i, " ")
        progress_panel.view.attroff(curses.color_pair(3))
        time.sleep(speed)


#s = init()
#create_stats_panel(s)
#create_equipped_panel(s)
#create_inventory_panel(s)
#create_log_panel(s)
#create_progress_panel(s)
#s.die()
