import random
import yaml
import config
import util
import objects

class Hero():
    def load_info(self, name):
        with open(config.SAVE_LOCATION + name, 'r') as f:
            self.__dict__ = yaml.load(f, Loader=yaml.Loader)

    def generate_new(self, name):
        random.seed()
        self.name = name
        self.lvl = 0
        self.next_lvl = 1
        self.exp_next_lvl = 1000
        self.exp = 0
        self.hp = random.randint(100,200)
        self.attack = random.randint(10,20)
        self.defense = random.randint(10,20)
        self.shitcoins = 0
        self.inventory = []

    def print_stats(self):
        print ("Name: {}".format(self.name))
        print ("Lvl: {}".format(self.lvl))
        print ("Next Lvl: {}".format(self.next_lvl))
        print ("Exp: {}".format(self.exp))
        print ("HP : {}".format(self.hp))
        print ("Att: {}".format(self.attack))
        print ("Def: {}".format(self.defense))
    
    def save_info(self):
        info = self.__dict__
        with open(config.SAVE_LOCATION + self.name, 'w') as f:
            yaml.dump(info, f)
    
    def level_up(self):
        self.lvl = self.next_lvl
        self.next_lvl = self.next_lvl + 1
        self.exp_next_lvl = int((self.exp - self.exp % 1000) + self.next_lvl * 1000)
        self.attack = self.attack + random.randint(5,10)
        self.defense = self.defense + random.randint(5,10)
        self.hp = self.hp + random.randint(10,30)

class Mob():
    def __init__(self, player_lvl):
        
        # Generate a new monster
        self._generate_new(player_lvl)

    def _generate_new(self, player_lvl):
        random.seed()
        self.name = random.choice(list(open(config.MOBS_LIST))).strip("\n")
        self.adjective = random.choice(list(open(config.MOB_ADJ_LIST))).strip("\n")
        self.lvl = max(1, random.randint(player_lvl - 5, player_lvl + 5))
        self.exp = 10 * self.lvl * util.modifier(player_lvl, self.lvl)
        self.hp = random.randint(50,200) * util.modifier(player_lvl, self.lvl) 
        self.shitcoins = int(self.lvl * util.modifier(player_lvl, self.lvl) + random.randint(0,10))
        self.loot_amount = random.randint(0,2)
        #self.attack = random.randint(10,20)
        self.defense = random.randint(10,20)

    

