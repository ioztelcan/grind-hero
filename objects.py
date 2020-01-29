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
        self._set_type()
        self.equipped = False
        self.att_bonus = 0
        self.def_bonus = 0

    def _set_type(self):
        random.seed()
        self.type = random.choice(config.ITEM_TYPES)

        if self.type == "weapon":
            self.name = random.choice(list(open(config.WEAPONS_LIST))).strip("\n")
            self.adjective = random.choice(list(open(config.WEAPON_ADJ_LIST))).strip("\n")
        
        elif self.type == "head":
            self.name = random.choice(list(open(config.HEAD_LIST))).strip("\n")
            self.adjective = random.choice(list(open(config.ARMOR_ADJ_LIST))).strip("\n")
        
        elif self.type == "body":
            self.name = random.choice(list(open(config.BODY_LIST))).strip("\n")
            self.adjective = random.choice(list(open(config.ARMOR_ADJ_LIST))).strip("\n")
        
        elif self.type == "item":
            self.name = random.choice(list(open(config.ITEMS_LIST))).strip("\n")
            self.adjective = random.choice(list(open(config.ITEM_ADJ_LIST))).strip("\n")

    def _generate_better(self):
        pass
