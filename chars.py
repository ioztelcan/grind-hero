import random
import yaml
import config
import util

def modifier(player_lvl, mob_lvl):
    diff = (mob_lvl - player_lvl)/10
    return 1 + diff

class Hero():
    def load_info(self, name):
        with open(config.SAVE_LOCATION + name, 'r') as f:
            self.__dict__ = yaml.safe_load(f)

    def generate_new(self, name):
        random.seed()
        self.name = name
        self.lvl = 0
        self.next_lvl = 1
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
        with open(config.SAVE_LOCATION + info["name"], 'w') as f:
            yaml.dump(info, f)


class Mob():
    def __init__(self, player_lvl):
        
        # Generate a new monster
        self._generate_new(player_lvl)

    def _generate_new(self, player_lvl):
        random.seed()
        self.name = random.choice(list(open('data/mobs'))).strip("\n")
        self.adjective = random.choice(list(open('data/mob-adj'))).strip("\n")
        self.lvl = random.randint(player_lvl - 5, player_lvl + 5)
        if self.lvl <= 0:
            self.lvl = 1
        self.exp = 10 * self.lvl * util.modifier(player_lvl, self.lvl)
        self.hp = random.randint(100,200)
        self.shitcoins = int(self.lvl * util.modifier(player_lvl, self.lvl) + random.randint(0,10))
        #self.attack = random.randint(10,20)
        self.defense = random.randint(10,20)

    

