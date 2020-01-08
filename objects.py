import config
import random

class Item():
    def __init__(self, lvl):
        self._generate_new(lvl)

    def _generate_new(self, lvl):
        self.name = random.choice(list(open(config.ITEMS_LIST))).strip("\n")
        self.adjective = random.choice(list(open(config.ITEM_ADJ_LIST))).strip("\n")
        self.lvl = max(1, random.randint(lvl - 5, lvl + 5)) 
        self.value = self.lvl * 10
        self.type = "placeholder"
        self.att_bonus = 0
        self.def_bonus = 0
