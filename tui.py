import curses
import os, sys
import time

stats_panel = None

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
        self.stdscr.addstr(self.height - 1, 0, "GRIND HERO v0.0.1 - Welcome to the grind yo.")
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
    scr = Screen()
    
    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    global stats_panel
    stats_panel = create_stats_panel(scr)
    create_equipped_panel(scr)
    create_inventory_panel(scr)
    create_log_panel(scr)
    create_progress_panel(scr)
    
    return scr

def create_stats_panel(screen):
    p = Panel(screen.height - 7, screen.quarter_w, screen.start_y, screen.start_x, "STATS")
    return p

def create_equipped_panel(screen):
    p = Panel(screen.height - 7, screen.quarter_w, screen.start_y, screen.start_x + screen.quarter_w, "EQUIPPED")
    return p

def create_inventory_panel(screen):
    p = Panel(screen.height - 1, screen.half_w, screen.start_y, screen.start_x + screen.half_w, "INVENTORY")
    return p

def create_log_panel(screen):
    p = Panel(3, screen.half_w, screen.height - 7, screen.start_x, "")
    return p

def create_progress_panel(screen):    
    p = Panel(3, screen.half_w, screen.height - 4, screen.start_x, "")
    return p

def update_stats_panel(hero):
    stats_panel.write(stats_panel.start_row,stats_panel.start_col,"HERO: {}".format(hero.name))
    stats_panel.write(stats_panel.start_row + 1,stats_panel.start_col,"HP: {}".format(hero.hp))
    stats_panel.write(stats_panel.start_row + 2,stats_panel.start_col,"ATT: {}".format(hero.attack))
    stats_panel.write(stats_panel.start_row + 3,stats_panel.start_col,"DEF: {}".format(hero.defense))
    stats_panel.write(stats_panel.start_row + 4,stats_panel.start_col,"NEXT_LVL: {}/{} ".format(hero.exp, hero.exp_next_lvl))
    

def init_tui():
    # Initialize curses settings.
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

       
    height, width = stdscr.getmaxyx()

    start_x = 0
    start_y = 0
    quarter_w = int(width // 4)
    half_w = int(width // 2)
    quarter_h = int(height // 4)
    half_h = int(height // 2)

    # lines, columns, start line, start column
    char_stats_w = Panel(half_h, quarter_w, start_y, start_x)
    char_stats_w.refresh()
    char_stats_w.view.addstr(char_stats_w.start_row,char_stats_w.start_col,"My string")
    char_stats_w.refresh()
    #return

    win2 = curses.newwin(half_h, quarter_w, start_y, start_x + quarter_w)
    win2.border()
    win2.refresh()

    win3= curses.newwin(half_h, half_w, start_y, start_x + half_w)
    win3.border()
    win3.refresh()

    win4 = curses.newwin(half_h, half_w, start_y + half_h, start_x)
    win4.border()
    win4.refresh()

    win5 = curses.newwin(half_h, half_w, start_y + half_h, start_x + half_w)
    win5.border()
    win5.refresh()


#s = init()
#create_stats_panel(s)
#create_equipped_panel(s)
#create_inventory_panel(s)
#create_log_panel(s)
#create_progress_panel(s)
#s.die()
