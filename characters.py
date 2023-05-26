from imports import *
try:
    from display import Color
except:
    pass


class Character:
    MAGE = 'Mage'
    WARRIOR = 'Warrior'
    RANGER = 'Ranger'

    character_list = []

    def __init__(self,
                 name:str,
                 max_health:int,
                 max_stamina:int,
                 max_mana:int,
                 attack:int,
                 armor:int,
                 armor_pen:float,
                 crit_rate:float,
                 crit_damage:float,
                 **scale_stats):
        Character.character_list.append(self)
        self.name = name
        self.stats = {
            'max_health' : max_health,
            'max_stamina': max_stamina,
            'max_mana': max_mana,
            'attack' : attack,
            'armor' : armor,
            'ArmorPenetration': armor_pen,
            'crit_rate' : crit_rate,
            'crit_damage' : crit_damage,
        }
        self.scale_stats = {}
        for name,value in scale_stats.items():
            if name in self.stats:
                self.scale_stats[name] = value
        self.abilities = []
    
    def print_stats(self):
        text = Text()
        for stat,value in self.stats.items():
            if stat[0:3] == "Max":
                if self.stats[stat] <= 0: continue
                text.append(f"{stat[3:len(stat)]} {value}\n")
            elif type(value) == float:
                text.append(f"{stat} {round(value*100)}%\n")
            elif type(value) == int:
                text.append(f"{stat} {value}\n")
            elif type(value) == str:
                text.append(f"{value}\n")
        return text


class CharacterDataBase:
    warrior = Character(Character.WARRIOR,
                        100,
                        50,
                        0,
                        10,
                        50,
                        0.08,
                        0.15,
                        1.5
    )
    mage = Character(Character.MAGE,
                    50,
                    50,
                    100,
                    25,
                    10,
                    0.27,
                    0.15,
                    1.5
    )
    ranger = Character(Character.RANGER,
                   70,
                   100,
                   50,
                   15,
                   20,
                   0.13,
                   0.23,
                   1.5
)


class Ability:
    def __init__(self, name: str, **cost) -> None:
        self.name = name
        self.cost = cost

    def use(self, caster, enemy):
        pass


class Damage(Ability):
    def __init__(self, name: str, damage_multiplayer:float=1.0, **cost) -> None:
        super().__init__(name, **cost)
        self.damage_multiplayer = damage_multiplayer

    def print_stats(self,caster):
        text = Text()
        text.append(f"{self.name}\n")
        text.append(f"Damage {int(caster.stats['Attack']*self.damage_multiplayer)}\n")
        if len(self.cost) != 0:
            text.append("Cost:\n")
        for name,value in self.cost.items():
            text.append(f"*{name} {value}\n")
        return text

    def can_use(self, caster):
        for name, value in self.cost.items():
            if caster.stats[name] - value < 0:
                return False
        return True

    def calculate_damage(self, attack, armor, armor_pen):
        armor -= armor*armor_pen
        reduction = 1+armor / 100
        result = attack*self.damage_multiplayer / reduction
        return int(result)
    
    def use(self, caster, target):
        text = Text()
        for name, value in self.cost.items():
            caster.stats[name] -= value
        attack = caster.stats['Attack']
        armor_pen = caster.stats['ArmorPen']
        crit_rate = caster.stats['CritRate']*100
        crit_damage = caster.stats['CritDamage']
        enemy_armor = target.stats['Armor']
        damage = self.calculate_damage(attack, enemy_armor, armor_pen)
        crit_roll = random.randrange(0,100)
        if crit_roll < crit_rate:
            text.append("!Critical hit!\n",style=Color.DANGER_COLOR)
            damage = int(damage * crit_damage)
        target.health -= damage
        text.append(f"{caster.name} dealt ")
        text.append(f"{damage} ",style=Color.DANGER_COLOR)
        text.append(f"Damage\n")
        return text


class AbilityDataBase:
    basic_attack = Damage("Basic attack",
                          1
    )
    heavy_attack = Damage("Heavy attack",
                          1.25,
                          stamina=10
    )


class Npc:
    pass


class Combat:
    def __init__(self,
                 max_health: int=100,
                 max_stamina: int=0,
                 max_mana: int=0,
                 attack: int=10,
                 armor: int=0,
                 armor_pen: float=0.0,
                 crit_rate: float=0.0,
                 crit_damage: float=1.0,
                 **scale_stats):
        self.level = {
            'level' : 1,
        }
        self.stats = {
            'MaxHealth' : max_health,
            'Health' : max_health,
            'Stamina': max_stamina,
            'MaxStamina': max_stamina,
            'Mana': max_mana,
            'MaxMana': max_mana,
            'Attack' : attack,
            'Armor' : armor,
            'ArmorPen': armor_pen,
            'CritRate' : crit_rate,
            'CritDamage' : crit_damage,
        }
        self.scale_stats = {}
        for name,value in scale_stats.items():
            if name in self.stats:
                self.scale_stats[name] = value
        self.status_effects = []

    
    def print_combat_stats(self):
        text = Text()
        text.append(f"level {self.stats['level']}\n")
        text.append(f"health {self.stats['health']}/{self.stats['max_health']}\n")
        if self.stats['max_stamina'] != 0:
            text.append(f"stamina {self.stats['stamina']}/{self.stats['max_stamina']}\n")
        if self.stats['max_mana'] != 0:
            text.append(f"mana {self.stats['mana']}/{self.stats['max_mana']}\n")
        text.append(f"attack {self.stats['attack']}\n")
        text.append(f"armor {self.stats['armor']}\n")
        text.append(f"armor_pen {round(self.stats['ArmorPenetration']*100)}%\n")
        text.append(f"crit_rate {round(self.stats['crit_rate']*100)}%\n")
        text.append(f"crit_damage {round(self.stats['crit_damage']*100)}%\n")
        return text

    @property
    def health(self):
        return self.stats['Health']
    
    @health.setter
    def health(self,value):
        self.stats['Health'] = value
        if self.stats['Health'] > self.stats['MaxHealth']:
            self.stats['Health'] = self.stats['MaxHealth']
        elif self.stats['Health'] < 0:
            self.stats['Health'] = 0
    
    @property
    def stamina(self):
        return self.stats['Stamina']
    
    @stamina.setter
    def stamina(self,value):
        self.stats['Stamina'] = value
        if self.stats['Stamina'] > self.stats['MaxStamina']:
            self.stats['Stamina'] = self.stats['MaxStamina']
        elif self.stats['Stamina'] < 0:
            self.stats['Stamina'] = 0
    
    @property
    def mana(self):
        return self.stats['Mana']
    
    @mana.setter
    def mana(self,value):
        self.stats['Mana'] = value
        if self.stats['Mana'] > self.stats['MaxMana']:
            self.stats['Mana'] = self.stats['MaxMana']
        elif self.stats['Mana'] < 0:
            self.stats['Mana'] = 0
    
    def calculate_damage(self,attack:int,armor:int,armor_pen:float):
        armor -= armor*armor_pen
        reduction = 1+armor/100
        result = attack/reduction
        return int(result)
    
    def damage(self,target):
        text = Text()
        attack = self.stats['Attack']
        armor_pen = self.stats['ArmorPen']
        crit_rate = self.stats['CritRate']*100
        crit_damage = self.stats['CritDamage']
        target_armor = target.stats['Armor']
        damage = self.calculate_damage(attack,target_armor,armor_pen)
        CritRoll = random.randrange(0,100)
        if CritRoll < crit_rate:
            text.append("!Critical hit!\n",style=Color.DANGER_COLOR)
            damage = int(damage * crit_damage)
        target.health -= damage
        text.append(f"{self.name} dealt ")
        text.append(f"{damage} ",style=Color.DANGER_COLOR)
        text.append(f"Damage\n")
        return text


class Enemy(Combat):
    def __init__(self,
                 name:str,
                 max_health: int,
                 max_stamina: int,
                 max_mana: int,
                 attack: int,
                 armor: int,
                 armor_pen: float,
                 crit_rate: float,
                 crit_damage: float,
                 **scale_stats):
        super().__init__(max_health,
                         max_stamina,
                         max_mana,
                         attack,
                         armor,
                         armor_pen,
                         crit_rate,
                         crit_damage,
                         **scale_stats)
        self.name = name
        from items import LootTable
        self.loot_table = LootTable()
        self.ExpDrop = 10
    
    def print_stats(self):
        text = Text()
        text.append(f"{self.name}\n")
        for stat,value in self.stats.items():
            if stat[0:3] == "Max": continue
            elif f'Max{stat}' in self.stats:
                if self.stats[f'Max{stat}'] <= 0: continue
                text.append(f"{stat} {value}/{self.stats[f'Max{stat}']}\n")
            elif type(value) == float:
                text.append(f"{stat} {round(value*100)}%\n")
            elif type(value) == int:
                text.append(f"{stat} {value}\n")
            elif type(value) == str:
                text.append(f"{value}\n")
        return text

from items import ItemDataBase as itemDB
class EnemyDataBase:
    dummy = Enemy("Dummy",
                100,
                0,
                0,
                5,
                0,
                0.0,
                0.0,
                1
    )
    dummy.loot_table.update({itemDB.coin:[0.5,1,50],
                            itemDB.leather_armor:[0.1,1],
                            itemDB.indel_staff:[0.01,1]})
    bandit = Enemy("Bandit",
                50,
                100,
                0,
                15,
                10,
                0.15,
                0.20,
                1.4
    )
    bandit.loot_table.update({itemDB.coin:[1,5],
                            itemDB.coin:[0.2,1,25],
                            itemDB.leather_armor:[0.5,1],
                            itemDB.iron_dagger:[1,1]})


class Player(Combat):
    def __init__(self):
        super().__init__()
        self.name = "Adventurer"
        self.class_ = None
        self.level = {
            'level': 1,
            'Exp': 0,
            'NeedExp': 100,
        }
        self.equipement_stats = {}
        self.equipment = {
            'Helmet': None,
            'Armor': None,
            'Primary': None,
            'Secondary': None,
        }
        self.inventory = []
        self.abilities = []
        self.location = {
            'x': 0,
            'y': 0,
        }
        self.tick = 0
        self.tick_game_update = 1
    
    @property
    def coins(self):
        for item in self.inventory:
            if item.id == itemDB.coin.id:
                return item.ammount
        return 0

    @coins.setter
    def coins(self, value):
        for item in self.inventory:
            if item.id == itemDB.coin.id:
                item.ammount = value
                return
        itemDB.coin.add_to_inventory(self.inventory, value)

    @property
    def exp(self):
        return self.stats['Exp']
    
    @exp.setter
    def exp(self,value):
        self.level['Exp'] = value
        if self.Exp >= self.level['NeedExp']:
            if self.level['level'] >= 40: 
                self.level['Exp'] = self.level['NeedExp']
                return
            self.level['level'] += 1
            overflow = self.exp - self.level['NeedExp']
            self.level['NeedExp'] = round((self.level['level']-1)**3+100)
            self.exp = overflow

    @property
    def x(self):
        return self.location['x']

    @x.setter
    def x(self, value):
        self.location['x'] = value
    
    @property
    def y(self):
        return self.location['y']

    @y.setter
    def y(self, value):
        self.location['y'] = value

    def get_position(self):
        return (self.location['x'],self.location['y'])

    def calculate_bonuses(self):
        #remove bonuses
        for name,value in self.equipement_stats.items():
            if name not in self.stats:
                continue
            self.stats[name] -= value
            self.equipement_stats[name] = 0
        
        #calculate equipment bonuses
        for slot in self.equipment:
            if self.equipment[slot] == None:
                continue
            item = self.equipment[slot]
            for name, value in item.stats.items():
                if name not in self.equipement_stats:
                    self.equipement_stats[name] = value
                    continue
                self.equipement_stats[name] += value

        #apply bonuses
        for name,value in self.equipement_stats.items():
            if name not in self.stats:
                continue
            self.stats[name] += value

    def print_stats(self):
        text = Text()
        text.append(f"Lvl {self.level['level']} ")
        text.append(f"{self.level['Exp']}/{self.level['NeedExp']}\n")
        for stat, value in self.stats.items():
            if stat[0:3] == "Max":
                continue
            elif f'Max{stat}' in self.stats:
                if self.stats[f'Max{stat}'] <= 0:
                    continue
                text.append(f"{stat} {value}/{self.stats[f'Max{stat}']}\n")
            elif type(value) == float:
                text.append(f"{stat} {round(value*100)}%\n")
            elif type(value) == int:
                text.append(f"{stat} {value}\n")
            elif type(value) == str:
                text.append(f"{value}\n")
        return text

    def equip_item(self, target_item):
        text = Text()
        item = target_item
        item_class = target_item.class_
        class_check = False
        item_slot = item.slot
        if item_class == None or item_class == self.stats['Class']:
            class_check = True
        for x in item_class:
            if x == self.stats['Class']:
                class_check = True
                break 
        if class_check == False:
            return text.append(f"Your class can't equip {item.name}")
        if self.equipment[item_slot] == None:
            self.equipment[item_slot] = item
            self.inventory = item.remove_from_inventory(self.inventory)
            self.calculate_bonuses()
            return text.append(f"{item.name} Equiped")
        else:
            equiped_item = self.equipment[item_slot]
            self.equipment[item_slot] = item
            self.inventory = item.remove_from_inventory(self.inventory)
            self.inventory = equiped_item.add_to_inventory(self.inventory)
            self.calculate_bonuses()
            return text.append(f"{item.name} Equiped\n{equiped_item.name} Unequiped")

    def unequip_Item(self, slot):
        item = self.equipment[slot]
        self.inventory = item.add_to_inventory(self.inventory)
        self.equipment[slot] = None
        self.calculate_bonuses()
        return Text(f"{item.name} Unequiped")

    def consume_item(self, item):
        # TODO THIS SHOULD BE IN ITEM CLASS
        return
        text = Text()
        match Item.Effect:
            case Potion.Effect.RESTORE:
                for name,value in Item.stats.items():
                    if name not in self.stats: continue
                    maxValue = self.stats[f"Max{name}"]
                    if maxValue == None:
                        text.append(f"Can't restore {name}\n")
                        continue
                    if self.stats[name] >= maxValue:
                        text.append(f"Your {name} is full\n")
                        continue
                    if type(value) == int:
                        self.stats[name] += value
                        text.append(f"{value} of {name} {Item.Effect}d")
                    elif type(value) == float:
                        self.stats[name] += int(maxValue*value)
                        text.append(f"{round(value*100)}% of {name} {Item.Effect}d")
            case _:
                return Text("Not yet implemented")
        self.Inventory = Item.remove_from_inventory(self.Inventory)
        return text

    def buy_item(self,
                 item,
                 ammount: int=1,
                 price_multiplayer: int=1):
        if item.sellable == False:
            return False
        if self.coins < item.get_price(ammount)*price_multiplayer:
            return False
        self.coins -= item.get_price(ammount)*price_multiplayer
        newItem = copy(item)
        self.inventory = newItem.add_to_inventory(self.inventory,ammount)
        return True

    def sell_item(self,
                  item,
                  ammount: int=1,
                  price_multiplayer: int=1):
        if item.sellable == False:
            return False
        self.coins += item.get_price(ammount)*price_multiplayer
        self.inventory = item.remove_from_inventory(self.inventory,ammount)
        return True

    def new_character(self, data):
        self.class_ = data.name
        for name, value in data.stats.items():

            if name in self.stats:
                if name[0:3] == "Max":
                    self.stats[name[3:len(name)]] = value
                self.stats[name] = value

