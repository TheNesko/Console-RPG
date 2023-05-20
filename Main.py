import win32gui, win32con, msvcrt, os, FontSize, json, pickle, random
from time import sleep
from os import system
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich import box
from math import floor,ceil
from copy import deepcopy as copy

GameVersion = "0.1"
SaveFilePath = os.getenv('APPDATA')+"\RPG_PYTHON"
if not os.path.exists(SaveFilePath):
    os.mkdir(SaveFilePath)

TEXT_COLOR = "green"
HIGHLIGHT_COLOR = "dark_green"
PANEL_COLOR = "white"
GO_BACK_COLOR = "dark_orange"
DANGER_COLOR = "red"
NEW_SAVE_FILE = "bright_blue"

layout = Layout()
layout.split_column(
Layout(name='MainTop',ratio=2,visible=False),
Layout(name='MainBottom',ratio=6)
)
layout['MainBottom'].split_column(
Layout(name='Game',ratio=2),
Layout(name='Map',ratio=6,visible=False)
)
layout['Game'].split_row(
Layout(name='Left',ratio=1),
Layout(name='Right',ratio=1)
)
layout["Left"].split_column(
Layout(name='TopL',ratio=2),
Layout(name='BottomL',ratio=6)
)
layout["Right"].split_column(
Layout(name='TopR',ratio=2),
Layout(name='BottomR',ratio=6)
)

class GameState:
    STARTING = 0
    LOADED = 1
    State = STARTING

class Key:
    KEY_tab = 9
    KEY_enter = 13
    KEY_ESC = 27
    KEY_space = 32
    KEY_plus = 43
    KEY_minus = 45
    KEY_0 = 48
    KEY_1 = 49
    KEY_2 = 50
    KEY_3 = 51
    KEY_4 = 52
    KEY_5 = 53
    KEY_6 = 54
    KEY_7 = 55
    KEY_8 = 56
    KEY_9 = 57
    KEY_EQUAL = 61
    KEY_FLOOR = 95
    KEY_a = 97
    KEY_d = 100
    KEY_e = 101
    KEY_n = 110
    KEY_q = 113
    KEY_s = 115
    KEY_w = 119
    KEY_y = 121
    KEY_del = 4301
    KEY_Aup = 4401
    KEY_Adown = 4402
    KEY_Aright = 4403
    KEY_Aleft = 4404

    @staticmethod
    def get_input():
        ky = msvcrt.getch()
        if ky in [b'\x00', b'\xe0']:
            ky = msvcrt.getch()
            if ky == b'S':
                return Key.KEY_del
            if ky == b'H':
                return Key.KEY_Aup
            if ky == b'P':
                return Key.KEY_Adown
            if ky == b'M':
                return Key.KEY_Aright
            if ky == b'K':
                return Key.KEY_Aleft
        return ord(ky.lower())


class ascii:
    @staticmethod
    def GameName(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('____ ___  ____    ____ ____ _  _ ____ \n',style=f'{Style}')
        text.append('|__/ |__] | __    | __ |__| |\/| |___ \n',style=f'{Style}')
        text.append('|  \ |    |__]    |__] |  | |  | |___ \n',style=f'{Style}')
        return text

    @staticmethod
    def NewGame(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('_  _ ____ _   _  ____ ____ _  _ ____ \n',style=f'{Style}')
        text.append('|\ | |___ | _ |  | __ |__| |\/| |___ \n',style=f'{Style}')
        text.append('| \| |___ |/ \|  |__] |  | |  | |___ \n',style=f'{Style}')
        return text
    
    @staticmethod
    def Credits(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('___ ____ ____ ___  _ ___ ____  \n',style=f'{Style}')
        text.append('|   |__/ |___ |  \ |  |  [___  \n',style=f'{Style}')
        text.append('|__ |  \ |___ |__/ |  |  ___]  \n',style=f'{Style}')
        return text
    
    @staticmethod
    def Load(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append('_   ____ ____ ___   \n',style=f'{Style}')
        text.append(' |   |  | |__| |  \ \n',style=f'{Style}')
        text.append(' |__ |__| |  | |__/ \n',style=f'{Style}')
        return text
    
    @staticmethod
    def Back(Style:str = "spring_green2"):
        text = Text("",justify="center")
        text.append(' ___  ____ ___ _  _\n',style=f'{Style}')
        text.append('|__\ |__| |   |_/ \n',style=f'{Style}')
        text.append('|__/ |  | |__ | \ \n',style=f'{Style}')
        return text


class CharacterClass:
    CharacterList = []
    def __init__(self,Name:str,MaxHealth:int,MaxStamina:int,MaxMana:int,Attack:int,Armor:int,ArmorPen:float,CritRate:float,CritDamage:float):
        CharacterClass.CharacterList.append(self)
        self.Statistics = {
            'Name' : Name,
            'MaxHealth' : MaxHealth,
            'MaxStamina': MaxStamina,
            'MaxMana': MaxMana,
            'Attack' : Attack,
            'Armor' : Armor,
            'ArmorPenetration': ArmorPen,
            'CritRate' : CritRate,
            'CritDamage' : CritDamage,
        }
    
    def PrintStats(self):
        text = Text()
        for stat,value in self.Statistics.items():
            if stat[0:3] == "Max":
                if self.Statistics[stat] <= 0: continue
                text.append(f"{stat[3:len(stat)]} {value}\n")
            elif type(value) == float:
                text.append(f"{stat} {round(value*100)}%\n")
            elif type(value) == int:
                text.append(f"{stat} {value}\n")
            elif type(value) == str:
                text.append(f"{value}\n")
        return text

Warrior = CharacterClass("Warrior",100,50,0,10,50,0.08,0.15,1.5)
Mage = CharacterClass("Mage",50,50,100,25,10,0.27,0.15,1.5)
Ranger = CharacterClass("Ranger",70,100,50,15,20,0.13,0.23,1.5)


class ItemClass:
    ItemList = []

    def __init__(self,Name:str="404Error",**Stats):
        if GameState.State == GameState.STARTING:
            self.ItemList.append(self)
        self._Name = Name
        self.id = hash(self._Name)
        self.Sellable = True
        self.Statistics = {}
        for Stat,value in Stats.items():
            self.Statistics[Stat] = value

    @property
    def Name(self):
        return self._Name
    
    @Name.setter
    def Name(self,value):
        self._Name = value

    def PrintStats(self,text):
        for stat in self.Statistics:
            if self.Statistics[stat] == None: continue
            if type(self.Statistics[stat]) == float:
                text.append(f"{stat}: {round(self.Statistics[stat]*100)}%\n")
            elif type(self.Statistics[stat]) == int:
                text.append(f"{stat}: {self.Statistics[stat]}\n")
            elif type(self.Statistics[stat]) == str:
                text.append(f"{self.Statistics[stat]}\n")
            elif type(self.Statistics[stat]) == type([]):
                text.append(f"{stat}: \n")
                for x in self.Statistics[stat]:
                    text.append(f"  *{x}\n")
        return text
    
    def getTypeName(self):
        return self.__class__.__name__

    def ItemToDictionary(self):
        Item = {
            'Name': self._Name,
            'Statistics': {}
        }
        for stat in self.Statistics:
            Item['Statistics'][stat] = self.Statistics[stat] 
        return Item

    @staticmethod
    def DictionaryToItem(dict):
        newItem = None
        match dict['Type']:
            case Equipment.__name__:
                newItem = Equipment(dict['Name'],dict['Price'],dict['Slot'],dict['Class'])
            case Potion.__name__:
                newItem = Potion(dict['Name'],dict['Price'],dict['Effect'])
            case Resource.__name__:
                newItem = Resource(dict['Name'],dict['BasePrice'],dict['Ammount'])
            case Currency.__name__:
                newItem = Currency(dict['Name'],dict['BasePrice'],dict['Ammount'])
        for stat in dict['Statistics']:
            newItem.Statistics[stat] = dict['Statistics'][stat]
        return newItem

    def GetPrice(self,Ammount:int=1):
        return self.Price*Ammount

    def Use(self,player):
        return Text("This item has no usage")
    
    def AddToInventory(self,Inventory,Ammount:int=1):
        Inventory.append(self)
        return Inventory
    
    def RemoveFromInventory(self,Inventory,Ammount:int=1):
        Inventory.remove(self)
        return Inventory

class Equipment(ItemClass):
    class Slot:
        HELMET = 'Helmet'
        ARMOR = 'Armor'
        PRIMARY = 'Primary'
        SECONDARY = 'Secondary'
    
    class Class:
        MAGE = Mage.Statistics['Name']
        WARRIOR = Warrior.Statistics['Name']
        RANGER = Ranger.Statistics['Name']

    def __init__(self, Name: str = "404Error",Price:int=1,Slot:str=Slot.PRIMARY,Class:str=None, **Stats):
        super().__init__(Name, **Stats)
        self.Price = Price
        self.Slot = Slot
        self.Class = Class
    
    def PrintStats(self):
        text = Text()
        text.append(f"{self.Name}\nPrice {self.Price}\nSlot: {self.Slot}\n")
        text.append("Class: ")
        if type(self.Class) == type([]):
            text.append("\n")
            for name in self.Class:
                text.append(f"*{name}\n")
        elif self.Class != None:
            text.append(f"{self.Class}\n")
        else: text.append("Any\n")
        return super().PrintStats(text)

    def ItemToDictionary(self):
        Item = {
            'Name': self._Name,
            'Type': self.getTypeName(),
            'Price': self.Price,
            'Slot': self.Slot,
            'Class': self.Class,
            'Statistics': {}
        }
        for stat in self.Statistics:
            Item['Statistics'][stat] = self.Statistics[stat] 
        return Item

    def Use(self, player):
        return player.EquipItem(self)

LeatherArmor = Equipment("Leather armor",70,Equipment.Slot.ARMOR,None,Armor=10)
IronDagger = Equipment("Iron Dagger",10,Equipment.Slot.SECONDARY,None,Attack=7,CritDamage=0.1)
ElvenShortbow = Equipment("Elven Shortbow",250,Equipment.Slot.PRIMARY,Equipment.Class.RANGER,Attack=5,CritRate=0.1)
WizzardHat = Equipment("Wizzard Hat",50,Equipment.Slot.HELMET,None,Armor=5,MaxMana=10)
IndelStaff = Equipment("Indel's Staff",2500,Equipment.Slot.PRIMARY,Equipment.Class.MAGE,Attack=20,CritDamage=0.2,CritRate=0.05)
BegginersWand = Equipment("Begginer's Wand",40,Equipment.Slot.PRIMARY,Equipment.Class.MAGE,Attack=5,ArmorPenetration=0.05)
MysticOrb = Equipment("Mystic Orb",150,Equipment.Slot.SECONDARY,Equipment.Class.MAGE,Attack=3,ArmorPenetration=0.08,CritRate=-0.03)
MageStudentCloak = Equipment("Mage Student's Cloak",100,Equipment.Slot.ARMOR,Equipment.Class.MAGE,Armor=10,MaxMana=20)
RoundShield = Equipment("Round Shield",100,Equipment.Slot.SECONDARY,Equipment.Class.WARRIOR,Armor=25,CritRate=-0.03,CritDamage=0.1)

class Potion(ItemClass):
    class Effect:
        RESTORE = 'Restore'

    def __init__(self, Name: str = "404Error",Price:int=1,Effect:str=Effect.RESTORE, **Stats):
        super().__init__(Name, **Stats)
        self.Price = Price
        self.Effect = Effect

    def PrintStats(self):
        text = Text()
        text.append(f"{self.Name}\nPrice: {self.Price}\n{self.Effect}\n")
        return super().PrintStats(text)
    
    def ItemToDictionary(self):
        Item = {
            'Name': self._Name,
            'Type': self.getTypeName(),
            'Price': self.Price,
            'Effect': self.Effect,
            'Statistics': {}
        }
        for stat in self.Statistics:
            Item['Statistics'][stat] = self.Statistics[stat] 
        return Item
    
    def Use(self, player):
        return player.ConsumeItem(self)

HealthRestore = Potion("Health restore",5,Potion.Effect.RESTORE,Health=0.3)
WeakManaRestore = Potion("Weak Mana restore",5,Potion.Effect.RESTORE,Mana=25)
ManaRestore = Potion("Mana restore",10,Potion.Effect.RESTORE,Mana=0.5)
FullHealthRestore = Potion("Angel's kiss",29,Potion.Effect.RESTORE,Health=1.0,Stamina=1.0,Mana=1.0)


class Resource(ItemClass):
    def __init__(self, Name: str = "404Error",BasePrice:int=1,Ammount:int=1, **Stats):
        super().__init__(Name, **Stats)
        self.BasePrice = BasePrice
        self.Ammount = Ammount
        self._Price = self.BasePrice * self.Ammount

    @property
    def Price(self):
        return self.BasePrice * self.Ammount
    
    @property
    def Name(self):
        if self.Ammount > 1: return f"{self._Name}s"
        return self._Name

    def PrintStats(self):
        text = Text()
        text.append(f"{self.Name}\nPrice: {self.BasePrice}\nFull Price: {self.Price}\nAmmount: {self.Ammount}")
        return super().PrintStats(text)

    def ItemToDictionary(self):
        Item = {
            'Name': self._Name,
            'Type': self.getTypeName(),
            'BasePrice': self.BasePrice,
            'Ammount': self.Ammount,
            'Statistics': {}
        }
        for stat in self.Statistics:
            Item['Statistics'][stat] = self.Statistics[stat] 
        return Item

    def GetPrice(self, Ammount: int = 1):
        return self.BasePrice*Ammount

    def AddToInventory(self,Inventory,Ammount:int=1):
        for index,item in enumerate(Inventory):
            if item.id == self.id:
                Inventory[index].Ammount += Ammount
                return Inventory
        newItem = copy(self)
        newItem.Ammount = Ammount
        Inventory.append(newItem)
        return Inventory

    def RemoveFromInventory(self,Inventory,Ammount:int=1):
        for index,item in enumerate(Inventory):
            if item == self:
                Inventory[index].Ammount -= Ammount
                if Inventory[index].Ammount <= 0:
                    Inventory.remove(self)
                return Inventory
        return Inventory

Log = Resource("Log",1)
Stone = Resource("Stone",2)
IronOre = Resource("Iron ore", 4)
IronBar = Resource("Iron bar", 12)

class Currency(Resource):
    def __init__(self, Name: str = "404Error", BasePrice: int = 1, Ammount: int = 1, **Stats):
        super().__init__(Name, BasePrice, Ammount, **Stats)
        self.Sellable = False
    
    def PrintStats(self):
        text = Text()
        text.append(f"{self.Name}\nAmmount: {self.Ammount}")
        return text

Coin = Currency("Coin")


class LootTable:
    def __init__(self,Loot={}) -> None:
        self.Loot = Loot
    
    def update(self,Items):
        self.Loot.update(Items)

    def RollItems(self):
        LootItems = {}
        for item,values in self.Loot.items():
            if values[0]*1000 <= random.randint(0,1000): continue
            if item not in LootItems: LootItems[item] = 0
            if len(values) == 2:
                LootItems[item] += values[1]
            elif len(values) == 1:
                LootItems[item] += 1
            else:
                LootItems[item] += random.randint(values[1],values[2])
        return LootItems
    
    def Drop(self,player):
        text = Text()
        DropItems = self.RollItems()
        LootAmmount = 0
        for item,ammount in DropItems.items():
            LootAmmount += 1
            item.AddToInventory(player.Inventory,ammount)
            text.append(f"{ammount}x {item.Name}\n" if ammount > 1 else f"{item.Name}\n")
        if LootAmmount == 0: return False
        return text


class Fight:
    def __init__(self,MaxHealth:int,MaxStamina:int,MaxMana:int,
                 Attack:int,Armor:int,ArmorPen:float,
                 CritRate:float,CritDamage:float,**ScaledStats):
        self.Statistics = {
            'Level' : 1,
            'MaxHealth' : MaxHealth,
            'Health' : MaxHealth,
            'Stamina': MaxStamina,
            'MaxStamina': MaxStamina,
            'Mana': MaxMana,
            'MaxMana': MaxMana,
            'Attack' : Attack,
            'Armor' : Armor,
            'ArmorPenetration': ArmorPen,
            'CritRate' : CritRate,
            'CritDamage' : CritDamage,
        }
        self.StatusEffects = []

    
    def PrintCombatStats(self):
        text = Text()
        text.append(f"Level {self.Statistics['Level']}\n")
        text.append(f"Health {self.Statistics['Health']}/{self.Statistics['MaxHealth']}\n")
        if self.Statistics['MaxStamina'] != 0:
            text.append(f"Stamina {self.Statistics['Stamina']}/{self.Statistics['MaxStamina']}\n")
        if self.Statistics['MaxMana'] != 0:
            text.append(f"Mana {self.Statistics['Mana']}/{self.Statistics['MaxMana']}\n")
        text.append(f"Attack {self.Statistics['Attack']}\n")
        text.append(f"Armor {self.Statistics['Armor']}\n")
        text.append(f"ArmorPen {round(self.Statistics['ArmorPenetration']*100)}%\n")
        text.append(f"CritRate {round(self.Statistics['CritRate']*100)}%\n")
        text.append(f"CritDamage {round(self.Statistics['CritDamage']*100)}%\n")
        return text

    @property
    def Health(self):
        return self.Statistics['Health']
    
    @Health.setter
    def Health(self,value):
        self.Statistics['Health'] = value
        if self.Statistics['Health'] > self.Statistics['MaxHealth']:
            self.Statistics['Health'] = self.Statistics['MaxHealth']
        elif self.Statistics['Health'] < 0:
            self.Statistics['Health'] = 0
    
    @property
    def Stamina(self):
        return self.Statistics['Stamina']
    
    @Stamina.setter
    def Stamina(self,value):
        self.Statistics['Stamina'] = value
        if self.Statistics['Stamina'] > self.Statistics['MaxStamina']:
            self.Statistics['Stamina'] = self.Statistics['MaxStamina']
        elif self.Statistics['Stamina'] < 0:
            self.Statistics['Stamina'] = 0
    
    @property
    def Mana(self):
        return self.Statistics['Mana']
    
    @Mana.setter
    def Mana(self,value):
        self.Statistics['Mana'] = value
        if self.Statistics['Mana'] > self.Statistics['MaxMana']:
            self.Statistics['Mana'] = self.Statistics['MaxMana']
        elif self.Statistics['Mana'] < 0:
            self.Statistics['Mana'] = 0

    def CalculateDamage(self,Attack:int,Armor:int,ArmorPen:float):
        Armor -= Armor*ArmorPen
        reduction = 1+Armor/100
        result = Attack/reduction
        return int(result)
    
    def Damage(self,Enemy):
        text = Text()
        Attack = self.Statistics['Attack']
        ArmorPen = self.Statistics['ArmorPenetration']
        CritRate = self.Statistics['CritRate']*100
        CritDamage = self.Statistics['CritDamage']
        EnemyArmor = Enemy.Statistics['Armor']
        Damage = self.CalculateDamage(Attack,EnemyArmor,ArmorPen)
        CritRoll = random.randrange(0,100)
        if CritRoll < CritRate:
            text.append("!Critical hit!\n",style=f"{DANGER_COLOR}")
            Damage = int(Damage * CritDamage)
        Enemy.Health -= Damage
        text.append(f"{self.Name} dealt ")
        text.append(f"{Damage} ",style=f"{DANGER_COLOR}")
        text.append(f"Damage\n")
        return text

    
class Enemy(Fight):
    def __init__(self,Name:str, MaxHealth: int, MaxStamina: int, MaxMana: int,
                Attack: int, Armor: int, ArmorPen: float,
                CritRate: float, CritDamage: float, **ScaledStats):
        super().__init__(MaxHealth, MaxStamina, MaxMana,
                         Attack, Armor, ArmorPen,
                         CritRate, CritDamage, **ScaledStats)
        self.Name = Name
        self.LootTable:LootTable = LootTable()
        self.ExpDrop = 10
        self.ScaledLevels = {}
        for stat,value in ScaledStats.items():
            self.ScaledLevels[stat] = value
    
    def PrintStats(self):
        text = Text()
        text.append(f"{self.Name}\n")
        for stat,value in self.Statistics.items():
            if stat[0:3] == "Max": continue
            elif f'Max{stat}' in self.Statistics:
                if self.Statistics[f'Max{stat}'] <= 0: continue
                text.append(f"{stat} {value}/{self.Statistics[f'Max{stat}']}\n")
            elif type(value) == float:
                text.append(f"{stat} {round(value*100)}%\n")
            elif type(value) == int:
                text.append(f"{stat} {value}\n")
            elif type(value) == str:
                text.append(f"{value}\n")
        return text

Dummy = Enemy("Dummy",100,0,0,5,0,0.0,0.0,1)
Dummy.LootTable.update({Coin:[0.5,1,50],LeatherArmor:[0.1,1],IndelStaff:[0.01,1]})
Bandit = Enemy("Bandit",50,100,0,15,10,0.15,0.20,1.4)
Bandit.LootTable.update({Coin:[1,5],Coin:[0.2,1,25],LeatherArmor:[0.5,1],IronDagger:[1,1]})

class Player(Fight):
    def __init__(self):
        self.Name = "Adventurer"
        self.Statistics = {
            'Class' : None,
            'Level' : 1,
            'Exp' : 0,
            'NeedExp' : 100,
            'MaxHealth' : 1,
            'Health' : 1,
            'Stamina': 1,
            'MaxStamina': 1,
            'Mana': 1,
            'MaxMana': 1,
            'Attack' : 1,
            'Armor' : 0,
            'ArmorPenetration': 0,
            'CritRate' : 0,
            'CritDamage' : 0,
        }
        self.Scaling = {}
        self.Inventory = []
        self.Equipment = {
            'Helmet' : None,
            'Armor' : None,
            'Primary' : None,
            'Secondary' : None,
        }
        self.Bonuses = {
            'MaxHealth' : 0,
            'Health' : 0,
            'Attack' : 0,
            'Armor' : 0,
            'ArmorPenetration': 0,
            'CritRate' : 0,
            'CritDamage' : 0,
        }
        self.Location = {
            'x' : 0,
            'y' : 0,
        }
        self.tick = 0
        self.tickGameUpdate = 1
    
    @property
    def Coins(self):
        for item in self.Inventory:
            if item.id == Coin.id:
                return item.Ammount
        return 0

    @Coins.setter
    def Coins(self,value):
        Coin.AddToInventory(self.Inventory,value)

    @property
    def Exp(self):
        return self.Statistics['Exp']
    
    @Exp.setter
    def Exp(self,value):
        self.Statistics['Exp'] = value
        if self.Exp >= self.Statistics['NeedExp']:
            if self.Statistics['Level'] >= 40: 
                self.Statistics['Exp'] = self.Statistics['NeedExp']
                return
            self.Statistics['Level'] += 1
            overflow = self.Exp - self.Statistics['NeedExp']
            self.Statistics['NeedExp'] = round((self.Statistics['Level']-1)**3+100)
            self.Exp = overflow

    def GetPosition(self):
        return (self.Location['x'],self.Location['y'])

    def CalculateBonuses(self):
        #remove bonuses
        for name,value in self.Bonuses.items():
            if name not in self.Statistics: continue
            self.Statistics[name] -= value
            self.Bonuses[name] = 0
        
        #calculate equipment bonuses
        for slot in self.Equipment:
            if self.Equipment[slot] == None: continue
            Item = self.Equipment[slot]
            for name,value in Item.Statistics.items():
                if name not in self.Bonuses:
                    self.Bonuses[name] = value
                    continue
                self.Bonuses[name] += value

        #apply bonuses
        for name,value in self.Bonuses.items():
            if name not in self.Statistics: continue
            self.Statistics[name] += value

    def PrintStats(self):
        text = Text()
        text.append(f"{self.Coins} Coins\n")
        for stat,value in self.Statistics.items():
            if stat[0:3] == "Max" or stat[0:4] == "Need": continue
            elif f'Max{stat}' in self.Statistics:
                if self.Statistics[f'Max{stat}'] <= 0: continue
                text.append(f"{stat} {value}/{self.Statistics[f'Max{stat}']}\n")
            elif f'Need{stat}' in self.Statistics:
                text.append(f"{stat} {value}/{self.Statistics[f'Need{stat}']}\n")
            elif type(value) == float:
                text.append(f"{stat} {round(value*100)}%\n")
            elif type(value) == int:
                text.append(f"{stat} {value}\n")
            elif type(value) == str:
                text.append(f"{value}\n")
        return text

    def EquipItem(self,TargetItem):
        text = Text()
        Item = TargetItem
        ItemClass = TargetItem.Class
        ClassCheck = False
        ItemSlot = Item.Slot
        if ItemClass == None or ItemClass == self.Statistics['Class']:  ClassCheck = True
        elif type(ItemClass) == type([]):
            for x in ItemClass:
                if x == self.Statistics['Class']:
                    ClassCheck = True
                    break 
        elif ItemClass != self.Statistics['Class']: return text.append(f"{Item.Name} is not for your Class")
        if ClassCheck == False: return text.append(f"{Item.Name} is not for your Class")
        if self.Equipment[ItemSlot] == None:
            self.Equipment[ItemSlot] = Item
            self.Inventory = Item.RemoveFromInventory(self.Inventory)
            self.CalculateBonuses()
            return text.append(f"{Item.Name} Equiped")
        else:
            EquipedItem = self.Equipment[ItemSlot]
            self.Equipment[ItemSlot] = Item
            self.Inventory = Item.RemoveFromInventory(self.Inventory)
            self.Inventory = EquipedItem.AddToInventory(self.Inventory)
            self.CalculateBonuses()
            return text.append(f"{Item.Name} Equiped\n{EquipedItem.Name} Unequiped")

    def UnequipItem(self,Slot):
        Item = self.Equipment[Slot]
        self.Inventory = Item.AddToInventory(self.Inventory)
        self.Equipment[Slot] = None
        self.CalculateBonuses()
        return Text(f"{Item.Name} Unequiped")

    def ConsumeItem(self,Item):
        text = Text()
        match Item.Effect:
            case Potion.Effect.RESTORE:
                for name,value in Item.Statistics.items():
                    if name not in self.Statistics: continue
                    maxValue = self.Statistics[f"Max{name}"]
                    if maxValue == None:
                        text.append(f"Can't restore {name}\n")
                        continue
                    if self.Statistics[name] >= maxValue:
                        text.append(f"Your {name} is full\n")
                        continue
                    if type(value) == int:
                        self.Statistics[name] += value
                        text.append(f"{value} of {name} {Item.Effect}d")
                    elif type(value) == float:
                        self.Statistics[name] += int(maxValue*value)
                        text.append(f"{round(value*100)}% of {name} {Item.Effect}d")
            case _:
                return Text("Not yet implemented")
        self.Inventory = Item.RemoveFromInventory(self.Inventory)
        return text

    def BuyItem(self,Item,Ammount:int=1,PriceMultiplayer:int=1):
        if self.Coins < Item.GetPrice(Ammount)*PriceMultiplayer: return False
        self.Coins -= Item.GetPrice(Ammount)*PriceMultiplayer
        newItem = copy(Item)
        self.Inventory = newItem.AddToInventory(self.Inventory,Ammount)
        return True

    def SellItem(self,Item,Ammount:int=1,PriceMultiplayer:int=1):
        if Item.Sellable == False: return False
        self.Coins += Item.GetPrice(Ammount)*PriceMultiplayer
        self.Inventory = Item.RemoveFromInventory(self.Inventory,Ammount)
        return True

    def NewCharacter(self,Data):
        self.Statistics['Class'] = Data.Statistics['Name']
        for name,value in Data.Statistics.items():
            if name in self.Statistics:
                if name[0:3] == "Max":
                    self.Statistics[name[3:len(name)]] = value
                self.Statistics[name] = value


class Game:
    @staticmethod
    def set_window(Title:str="Window",Colums:int=80,Lines:int=30):
        system('mode con: cols=%i lines=%i' %(Colums,Lines))
        system("title %s" % Title)
    
    @staticmethod
    def set_window_size(Colums:int=80,Lines:int=30):
        system('mode con: cols=%i lines=%i' %(Colums,Lines))
    
    @staticmethod
    def disable_quickedit():
        '''Disable quickedit mode on Windows terminal. quickedit prevents script to
        run without user pressing keys..'''
        if not os.name == 'posix':
            try:
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                device = r'\\.\CONIN$'
                with open(device, 'r') as con:
                    hCon = msvcrt.get_osfhandle(con.fileno())
                    kernel32.SetConsoleMode(hCon, 0x0080)
            except Exception as e:
                print('Cannot disable QuickEdit mode! ' + str(e))

    @staticmethod
    def disable_window_resize():
        # get the handle of the window you want to disable resizing for
        hwnd = win32gui.FindWindow(None, 'Rpg game')
        # get the current window style
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        # disable the resizable flag in the window style
        style &= ~win32con.WS_THICKFRAME
        # update the window style
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
        # force the window to redraw with the new style
        win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE |
                            win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)

    @staticmethod
    def update_layout(LayoutName:str,content="",title=None,ratio=None,visible=True,border=box.MINIMAL):
        layout[LayoutName].update(Panel(content,title=title,style=PANEL_COLOR,box=border))
        if ratio != None: layout[LayoutName].ratio = ratio
        layout[LayoutName].visible = visible

    @staticmethod
    def layoutToggleVisible(LayoutName:str,visible:bool=None):
        if visible == None: layout[LayoutName].visible = not layout[LayoutName].visible
        else: layout[LayoutName].visible = visible

    def Tick(self):
        self.player.tick += 1
        if self.player.tick >= self.player.tickGameUpdate:
            self.player.tickGameUpdate = self.player.tick + random.randint(7,14)
            # DO GAME UPDATES
            self.GenerateShopItems()

    def OptionsToText(self,Options,Target=0):
        text = Text("",justify="left")
        for index,option in enumerate(Options):
            if index == len(Options)-1 and Target == index:
                text.append(f">{index+1}.{option}\n",f"u {GO_BACK_COLOR}")
            elif index == Target:
                text.append(f">{index+1}.{option}\n",f"u {HIGHLIGHT_COLOR}")
            else:
                text.append(f"{index+1}.{option}\n",TEXT_COLOR)
        return text

    def ConfirmScreen(self,text:Text):
        self.update_layout("MainTop",text)
        if Key.get_input() == Key.KEY_y:
            return True
        return False

    def ChangeTarget(self,PressedKey,currentTarget,Options):
        match PressedKey:
            case Key.KEY_Adown | Key.KEY_s:
                currentTarget += 1
                if currentTarget > len(Options)-1: currentTarget = 0
            case Key.KEY_Aup | Key.KEY_w:
                currentTarget -= 1
                if currentTarget < 0: currentTarget = len(Options)-1
        return currentTarget

    def StartScreen(self):
        menus = [self.PlayScreen, self.SettingsScreen, self.CreditsScreen]
        options = ["Play","Options","Credits","Exit"]
        target = 0
        while True:
            GameName = ascii.GameName()
            OptionScreen = self.OptionsToText(options,target)
            self.update_layout("TopL",GameName,ratio=2)
            self.update_layout("TopR","",ratio=1)
            self.update_layout("BottomL",OptionScreen,ratio=6)
            self.update_layout("BottomR","",ratio=1)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=0)
            pressedKey = Key.get_input()
            target = self.ChangeTarget(pressedKey,target,options)
            match pressedKey:
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1: return
                    else: menus[target]()
                case Key.KEY_ESC:
                    return
    
    Settings = {'FontSize':22,'CombatSpeed':1}
    def SettingsScreen(self):
        options = []
        for name in self.Settings:
            options.append(name)
        options.append("Back")
        target = 0
        while True:
            OptionsText = Text("\n\n",justify="center")
            
            for index,name in enumerate(options):
                if index == len(options)-1 and target == index:
                    OptionsText.append(f"{name}\n",style=f"u {GO_BACK_COLOR}")
                elif index == target:
                    OptionsText.append(f"<- - {name} [{self.Settings[name]}] + ->\n", style=f"u {HIGHLIGHT_COLOR}")
                elif index == len(options)-1:
                    OptionsText.append(f"{name}\n", style=f"{TEXT_COLOR}")
                else:
                    OptionsText.append(f"{name} [{self.Settings[name]}]\n", style=f"{TEXT_COLOR}")

            self.update_layout("TopL",OptionsText,title="Press ESC to exit",ratio=1)
            self.update_layout("TopR","",ratio=1)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=1)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=0)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_Aleft | Key.KEY_a:
                    match target:
                        case 0:
                            FontSize.run(max(FontSize.getFontSize()-1,10))
                            self.Settings['FontSize'] = FontSize.getFontSize()
                        case 1:
                            self.Settings['CombatSpeed'] = max(self.Settings['CombatSpeed']-1,1)
                case Key.KEY_Aright | Key.KEY_d:
                    match target:
                        case 0:
                            FontSize.run(min(FontSize.getFontSize()+1,30))
                            self.Settings['FontSize'] = FontSize.getFontSize()
                        case 1:
                            self.Settings['CombatSpeed'] = min(self.Settings['CombatSpeed']+1,5)
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1: break
                case Key.KEY_ESC:
                    break
        with open("Settings.json", "w") as write_file:
            json.dump(self.Settings, write_file)
            write_file.close()

    def CreditsScreen(self):
        CreditsText = [
            "=====Developement=====",
            "Director: CursedIndel",
            "Design: CursedIndel",
            "Code: CursedIndel",
            "Art: CursedIndel",
            "Writing: CursedIndel",
            "Translation: CursedIndel",
            "",
            "========Testers========",
            "CursedIndel",
            "Your Mom",
            "",
            "========Sponsors========",
            "Your Mom",
            "Spodermon",
        ]
        target = 0
        while True:
            InfoScreen = ascii.Credits()
            LeftScreen = Text("",no_wrap=False,justify="center")
            for index in range(target,len(CreditsText)):
                LeftScreen.append(f"{CreditsText[index]}\n",f"{TEXT_COLOR}")
            self.update_layout("TopL",InfoScreen,ratio=2)
            self.update_layout("TopR","",ratio=1)
            self.update_layout("BottomL",LeftScreen,"press ESC to exit",ratio=6)
            self.update_layout("BottomR","",ratio=1)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=0)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(CreditsText)-1: target = len(CreditsText)-1
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = 0
                case Key.KEY_ESC | Key.KEY_enter | Key.KEY_space:
                    return
    
    def PlayScreen(self):
        menus = [self.NewGameScreen,self.ContinueSave,self.LoadScreen]
        options = ["New game","Continue","Load","Back"]
        target = 0
        while True:
            match target:
                case 0:
                    InfoScreen = ascii.NewGame()
                case 1 | 2:
                    InfoScreen = ascii.Load()
                case 3:
                    InfoScreen = ascii.Back()
            LeftScreen = self.OptionsToText(options,target)
            self.update_layout("TopL",InfoScreen,ratio=2)
            self.update_layout("TopR","",ratio=1)
            self.update_layout("BottomL",LeftScreen,ratio=6)
            self.update_layout("BottomR","",ratio=1)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=0)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1: return
                    else:
                        self.player = Player()
                        if menus[target]() != None:
                            self.MainScreen()
                case Key.KEY_ESC:
                    return
    
    def NewGameScreen(self):
        options = []
        for x in CharacterClass.CharacterList:
            options.append(x.Statistics['Name'])
        options.append("Back")
        target = 0
        while True:
            InfoScreen = self.OptionsToText(options,target)
            if target <= len(CharacterClass.CharacterList)-1:
                CharactersDescriptions = CharacterClass.CharacterList[target].PrintStats()
            else:
                CharactersDescriptions = ascii.Back()
            self.update_layout("TopL",InfoScreen,ratio=2)
            self.update_layout("TopR",CharactersDescriptions,ratio=2)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=2)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1:
                        return
                    else:
                        self.player.NewCharacter(CharacterClass.CharacterList[target])
                        if self.NameCharacterScreen(): return
                        return True
                case Key.KEY_ESC:
                    return

    def NameCharacterScreen(self):
        PlayerName = ""
        while True:
            NamingScreen = Text(f"\nName your character\n",justify="center")
            NamingScreen.append(f"{PlayerName}" if PlayerName != "" else f"'{self.player.Name}'")
            self.update_layout("TopL",ratio=2)
            self.update_layout("TopR","",ratio=0)
            self.update_layout("BottomL",NamingScreen,f"You choose {self.player.Statistics['Class']}",ratio=6)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=0)
            userInput = msvcrt.getwch()
            if userInput == '\r':
                if PlayerName != "":
                    self.player.Name = PlayerName
                break
            elif userInput == '\x08':
                PlayerName = PlayerName[:-1]
            elif userInput == '\t' or userInput == '\x00':
                pass
            elif userInput == '\x1b':
                return True
            elif len(PlayerName) < 22:
                PlayerName += str(userInput)

    def MainScreen(self):
        self.Tick()
        target = 0
        while True:
            menus = [self.TravelScreen,self.InventoryScreen,self.SaveScreen]
            options = ["Travel","Inventory","Save","Menu"]
            InfoScreen = self.OptionsToText(options,target)
            DescriptionScreen = self.player.PrintStats()
            self.update_layout("TopL",InfoScreen,f"Location: {Map.GetTile(self.player.GetPosition()).Name}",ratio=1)
            self.update_layout("TopR",DescriptionScreen,self.player.Name,ratio=1)
            self.update_layout("BottomL","",ratio=1)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1: return
                    else:
                        if menus[target](): return True
                case Key.KEY_ESC:
                    return

    def TravelScreen(self):
        while True:
            tileInfo = Map.GetTile(self.player.GetPosition()).DisplayTileInfo()
            mapScreen = Map.DisplayMap(self.player.GetPosition())
            mapScreen.justify = "center"
            mapLegend = Text()
            for tile in GameTileBase:
                mapLegend.append(f"{tile.MapSymbol}",style=f"{tile.MapColor}")
                mapLegend.append(f" - {tile.Name}\n")
            self.update_layout("TopL",tileInfo,"Tile info",ratio=1)
            self.update_layout("TopR",mapLegend,"Legend",ratio=1)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            self.update_layout("Map",mapScreen,"Map",border=box.ASCII2)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    self.player.Location['y'] += 1
                    if self.player.Location['y'] > Map.Height-1:self.player.Location['y'] = Map.Height-1
                    else: self.Tick()
                case Key.KEY_Aup | Key.KEY_w:
                    self.player.Location['y'] -= 1
                    if self.player.Location['y'] < 0: self.player.Location['y'] = 0
                    else: self.Tick()
                case Key.KEY_Aright | Key.KEY_d:
                    self.player.Location['x'] += 1
                    if self.player.Location['x'] > Map.Width-1: self.player.Location['x'] = Map.Width-1
                    else: self.Tick()
                case Key.KEY_Aleft | Key.KEY_a:
                    self.player.Location['x'] -= 1
                    if self.player.Location['x'] < 0: self.player.Location['x'] = 0
                    else: self.Tick()
                case Key.KEY_enter | Key.KEY_space:
                    if self.ActivityScreen():
                        self.update_layout("Map",visible=False)
                        return True
                case Key.KEY_ESC | Key.KEY_tab:
                    break
        self.update_layout("Map",visible=False)

    def ActivityScreen(self):
        MapTile = Map.GetTile(self.player.GetPosition())
        if MapTile.Content == {}: return
        target = 0
        while True:
            menus = []
            options = []
            for name,value in MapTile.Content.items():
                if type(value) == bool: continue
                menus.append(value)
                options.append(name)
            if menus == []: return
            options.append("Back")
            optionsText = self.OptionsToText(options,target)
            self.update_layout("TopL",optionsText,"Activities",ratio=1)
            self.update_layout("TopR",ratio=0)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    self.layoutToggleVisible("Map",False)
                    if target == len(options)-1: break
                    else:
                        if menus[target](): return True
                    self.layoutToggleVisible("Map",True)
                case Key.KEY_ESC:
                    break
        self.update_layout("Map",visible=False)

    def FightScreen(self):
        self.layoutToggleVisible("Map",True)
        MapTile = Map.GetTile(self.player.GetPosition())
        Enemy = None
        EnemyFindRoll = 0.4
        if MapTile.Hostile == True: EnemyFindRoll = 0.8
        if (EnemyFindRoll*100) > random.randrange(0,100) and MapTile.PossibleEnemies != []:
            Enemy = copy(MapTile.PossibleEnemies[random.randint(0,len(MapTile.PossibleEnemies)-1)])
        if Enemy == None:
            text = Text("\n\nThere are no enemies around",justify='center',style=f"{DANGER_COLOR}")
            self.update_layout("TopL",text,"Press any key to continue",ratio=1)
            self.update_layout("Right",ratio=0)
            self.Tick()
            Key.get_input()
            return
        target = 0
        options = [Enemy.Name,"Back"]
        while True:
            text = self.OptionsToText(options,target)
            self.update_layout("TopL",text,ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    self.layoutToggleVisible("Map",False)
                    if target == len(options)-1: break
                    if self.CombatScreen(Enemy): return True
                    self.layoutToggleVisible("Map",True)
                    break
                case Key.KEY_ESC:
                    break
    
    def CombatScreen(self,Enemy:Enemy):
        options = ["Attack","Inventory","Escape"]
        target = 0
        while True:
            optionsText = self.OptionsToText(options,target)
            self.update_layout("MainTop",optionsText,ratio=2)
            self.update_layout("TopL",ratio=0)
            self.update_layout("TopR",ratio=0)
            self.update_layout("BottomL",self.player.PrintCombatStats(),self.player.Name,ratio=6)
            self.update_layout("BottomR",Enemy.PrintCombatStats(),Enemy.Name,ratio=6)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    match target:
                        case 0:
                            # PLAYER TURN
                            CombatText = self.player.Damage(Enemy)
                            self.update_layout("MainTop",CombatText,"Combat in progress",ratio=2)
                            self.update_layout("BottomR",Enemy.PrintCombatStats(),Enemy.Name,ratio=6)
                            sleep(1/self.Settings['CombatSpeed'])
                            if Enemy.Health == 0:
                                CombatText.append(f"{Enemy.Name} has been defeated\n+{Enemy.ExpDrop}Exp")
                                self.update_layout("MainTop",CombatText,"Press any key to continue",ratio=2)
                                Key.get_input()
                                # DROP LOOT AND SHIT
                                self.player.Exp += Enemy.ExpDrop
                                CombatText = Enemy.LootTable.Drop(self.player)
                                if CombatText == False: break
                                self.update_layout("MainTop",CombatText,"Press any key to continue",ratio=2)
                                Key.get_input()
                                break
                            # ENEMY TURN
                            CombatText.append(Enemy.Damage(self.player))
                            self.update_layout("MainTop",CombatText,"Combat in progress",ratio=2)
                            self.update_layout("BottomL",self.player.PrintCombatStats(),self.player.Name,ratio=6)
                            sleep(1/self.Settings['CombatSpeed'])
                            if self.player.Health == 0:
                                CombatText.append(f"You have been defeated")
                                # FUCKING DIE LOL
                                self.update_layout("MainTop",CombatText,"Press any key to continue",ratio=2)
                                Key.get_input()
                                self.update_layout("MainTop",ratio=0)
                                return True
                            sleep(1/self.Settings['CombatSpeed'])
                        case 1:
                            self.update_layout("MainTop",ratio=0)
                            self.InventoryScreen()
                        case 2:
                            break
        self.update_layout("MainTop",ratio=0)
    
    def InventoryScreen(self):
            activeWindow = 0 # 0-inventory 1-equipment
            currentPage = 0
            itemsPerPage = 25
            targetInventory = 0
            targetEquipement = 0
            while True:
                InfoScreen = Text()
                InventoryScreen = Text()
                EquipementScreen = Text()
                Pages = [[]]
                LoopPage = 0 # on what page for loop currently is
                for item in self.player.Inventory:
                    if len(Pages[LoopPage]) >= itemsPerPage:
                        LoopPage += 1
                        Pages.append([])
                    Pages[LoopPage].append(item)

                if currentPage > len(Pages)-1:
                    currentPage = len(Pages)-1
                    targetInventory = len(Pages[currentPage])-1

                targetItem = None
                targetSlot = None
                if activeWindow == 0:
                    ExitIndex = len(Pages[currentPage])
                    if targetInventory > ExitIndex: targetInventory = ExitIndex
                else:
                    ExitIndex = len(self.player.Equipment)
                    if targetEquipement > ExitIndex: targetEquipement = ExitIndex

                if len(Pages[currentPage]) > 0:
                    for index, Item in enumerate(Pages[currentPage]):
                        if index == targetInventory and activeWindow == 0: 
                            InventoryScreen.append(f">{Item.Name}\n" ,style=f"u {HIGHLIGHT_COLOR}")
                            targetItem = Item
                            InfoScreen.append(targetItem.PrintStats())
                        else: InventoryScreen.append(f"{Item.Name}\n" ,style=f"{TEXT_COLOR}")
                if targetInventory == ExitIndex and activeWindow == 0: InventoryScreen.append(">Back\n" ,style=f"u {GO_BACK_COLOR}")
                elif activeWindow == 0: InventoryScreen.append("Back\n" ,style=f"{TEXT_COLOR}")

                for index, slot in enumerate(self.player.Equipment):
                    if index == targetEquipement and activeWindow == 1:
                        if self.player.Equipment[slot] != None:
                            EquipementScreen.append(f"{slot}: {self.player.Equipment[slot].Name}\n" ,style=f"u {HIGHLIGHT_COLOR}")
                            targetItem = self.player.Equipment[slot]
                            InfoScreen.append(targetItem.PrintStats())
                        else: EquipementScreen.append(f"{slot}: {self.player.Equipment[slot]}\n" ,style=f"u {HIGHLIGHT_COLOR}")
                        targetSlot = slot
                    else:
                        if self.player.Equipment[slot] != None: EquipementScreen.append(f"{slot}: {self.player.Equipment[slot].Name}\n" ,style=f"{TEXT_COLOR}")
                        else: EquipementScreen.append(f"{slot}: {self.player.Equipment[slot]}\n" ,style=f"{TEXT_COLOR}")
                if targetEquipement == ExitIndex and activeWindow == 1: EquipementScreen.append(">Back\n" ,style=f"u {GO_BACK_COLOR}")
                elif activeWindow == 1: EquipementScreen.append("Back\n" ,style=f"{TEXT_COLOR}")

                if targetInventory == ExitIndex and activeWindow == 0: InfoScreen = self.player.PrintStats()
                if targetEquipement == ExitIndex and activeWindow == 1: InfoScreen = self.player.PrintStats()

                self.update_layout("TopL",InventoryScreen,f"Inventory Page {currentPage+1}/{len(Pages)}",ratio=1)
                self.update_layout("TopR",EquipementScreen,"Equipment",ratio=2)
                self.update_layout("BottomL","",ratio=0)
                self.update_layout("BottomR",InfoScreen,"Description" if targetItem != None else None,ratio=6)
                self.update_layout("Left",ratio=1)
                self.update_layout("Right",ratio=1)
                match Key.get_input():
                    case Key.KEY_Adown | Key.KEY_s:
                        if activeWindow == 0:
                            targetInventory += 1
                            if targetInventory > ExitIndex:
                                targetInventory = 0
                                currentPage += 1
                                if currentPage > len(Pages)-1:
                                    currentPage = 0
                                    targetInventory = ExitIndex
                        else:
                            targetEquipement += 1
                            if targetEquipement > ExitIndex:
                                targetEquipement = ExitIndex
                    case Key.KEY_Aup | Key.KEY_w:
                        if activeWindow == 0:
                            targetInventory -= 1
                            if targetInventory < 0:
                                currentPage -= 1
                                targetInventory = len(Pages[currentPage])
                                if currentPage < 0 :
                                    currentPage = len(Pages)-1
                                    targetInventory = 0
                        else:
                            targetEquipement -= 1
                            if targetEquipement < 0:
                                targetEquipement = 0
                    case Key.KEY_a | Key.KEY_Aleft:
                        activeWindow -= 1
                        if activeWindow < 1: activeWindow = 0
                    case Key.KEY_d | Key.KEY_Aright:
                        activeWindow += 1
                        if activeWindow > 1: activeWindow = 1
                    case Key.KEY_tab:
                        activeWindow += 1
                        if activeWindow > 1: activeWindow = 0
                    case Key.KEY_enter | Key.KEY_space:
                        if activeWindow == 0 and targetInventory == ExitIndex:
                            return
                        elif activeWindow == 1 and targetEquipement == ExitIndex:
                            return
                        elif activeWindow == 0 and targetItem != None:
                            self.update_layout("BottomR",targetItem.Use(self.player),title="Press ANY key")
                            Key.get_input()
                        elif activeWindow == 1 and targetItem != None:
                            self.update_layout("BottomR",self.player.UnequipItem(targetSlot),title="Press ANY key")
                            Key.get_input()
                    case Key.KEY_ESC:
                        return

    def GenerateShopItems(self):
        self.shopInventory = []
        for x in range(50):
            newItem = copy(ItemClass.ItemList[random.randint(0,len(ItemClass.ItemList)-1)])
            self.shopInventory = newItem.AddToInventory(self.shopInventory)

    shopInventory = []
    def ShopScreen(self):
        shopItems = self.shopInventory
        activeWindow = 0 # 0-inventory 1-shop
        currentInventoryPage = 0
        currentShopPage = 0
        itemsPerPage = 15
        targetInventory = 0
        targetShop = 0
        while True:
            InfoScreen = Text()
            InventoryScreen = Text()
            ShopScreen = Text()
            InventoryPages = [[]]
            LoopPage = 0 # on what page for loop currently is
            for item in self.player.Inventory:
                if len(InventoryPages[LoopPage]) >= itemsPerPage:
                    LoopPage += 1
                    InventoryPages.append([])
                InventoryPages[LoopPage].append(item)
            LoopPage = 0
            ShopPages = [[]]
            for item in shopItems:
                if len(ShopPages[LoopPage]) >= itemsPerPage:
                    LoopPage += 1
                    ShopPages.append([])
                ShopPages[LoopPage].append(item)

            if currentInventoryPage > len(InventoryPages)-1:
                currentInventoryPage = len(InventoryPages)-1
                targetInventory = len(InventoryPages[currentInventoryPage])-1
            if currentShopPage > len(ShopPages)-1:
                currentShopPage = len(ShopPages)-1
                targetShop = len(ShopPages[currentShopPage])-1

            targetItem = None
            if activeWindow == 0:
                ExitIndex = len(InventoryPages[currentInventoryPage])
                if targetInventory > ExitIndex: targetInventory = ExitIndex
            else:
                ExitIndex = len(ShopPages[currentShopPage])
                if targetShop > ExitIndex: targetShop = ExitIndex

            if len(InventoryPages[currentInventoryPage]) > 0:
                for index, Item in enumerate(InventoryPages[currentInventoryPage]):
                    if index == targetInventory and activeWindow == 0: 
                        InventoryScreen.append(f">{Item.Name}\n" ,style=f"u {HIGHLIGHT_COLOR}")
                        targetItem = Item
                        InfoScreen.append(targetItem.PrintStats())
                    else: InventoryScreen.append(f"{Item.Name}\n" ,style=f"{TEXT_COLOR}")
            if targetInventory == ExitIndex and activeWindow == 0: InventoryScreen.append(">Back\n" ,style=f"u {GO_BACK_COLOR}")
            elif activeWindow == 0: InventoryScreen.append("Back\n" ,style=f"{TEXT_COLOR}")

            if len(ShopPages[currentShopPage]) > 0:
                for index, Item in enumerate(ShopPages[currentShopPage]):
                    if index == targetShop and activeWindow == 1: 
                        ShopScreen.append(f">{Item.Name}\n" ,style=f"u {HIGHLIGHT_COLOR}")
                        targetItem = Item
                        InfoScreen.append(targetItem.PrintStats())
                    else: ShopScreen.append(f"{Item.Name}\n" ,style=f"{TEXT_COLOR}")
            if targetShop == ExitIndex and activeWindow == 1: ShopScreen.append(">Back\n" ,style=f"u {GO_BACK_COLOR}")
            elif activeWindow == 1: ShopScreen.append("Back\n" ,style=f"{TEXT_COLOR}")

            if activeWindow == 0 and targetInventory == ExitIndex:
                InfoScreen.append(ascii.Back())
                InfoScreen.justify='center'
            if activeWindow == 1 and targetShop == ExitIndex:
                InfoScreen.append(ascii.Back())
                InfoScreen.justify='center'

            self.update_layout("MainTop",InfoScreen,f"{self.player.Coins} Coins",ratio=3)
            self.update_layout("TopL",ratio=0)
            self.update_layout("TopR",ratio=0)
            self.update_layout("BottomL",InventoryScreen,f"Inventory Page {currentInventoryPage+1}/{len(InventoryPages)}",ratio=6)
            self.update_layout("BottomR",ShopScreen,f"Shop Page {currentShopPage+1}/{len(ShopPages)}",ratio=6)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    if activeWindow == 0:
                        targetInventory += 1
                        if targetInventory > ExitIndex:
                            targetInventory = 0
                            currentInventoryPage += 1
                            if currentInventoryPage > len(InventoryPages)-1:
                                currentInventoryPage = len(InventoryPages)-1
                                targetInventory = ExitIndex
                    else:
                        targetShop += 1
                        if targetShop > ExitIndex: 
                            targetShop = 0
                            currentShopPage += 1
                            if currentShopPage > len(ShopPages)-1:
                                currentShopPage = len(ShopPages)-1
                                targetShop = ExitIndex
                case Key.KEY_Aup | Key.KEY_w:
                    if activeWindow == 0:
                        targetInventory -= 1
                        if targetInventory < 0:
                            currentInventoryPage -= 1
                            targetInventory = len(InventoryPages[currentInventoryPage])-1
                            if currentInventoryPage < 0 :
                                currentInventoryPage = 0
                                targetInventory = 0
                    else:
                        targetShop -= 1
                        if targetShop < 0:
                            currentShopPage -= 1
                            targetShop = len(ShopPages[currentShopPage])-1
                            if currentShopPage < 0 :
                                currentShopPage = 0
                                targetShop = 0
                case Key.KEY_a | Key.KEY_Aleft:
                    activeWindow -= 1
                    if activeWindow < 1: activeWindow = 0
                case Key.KEY_d | Key.KEY_Aright:
                    activeWindow += 1
                    if activeWindow > 1: activeWindow = 1
                case Key.KEY_tab:
                    activeWindow += 1
                    if activeWindow > 1: activeWindow = 0
                case Key.KEY_enter | Key.KEY_space:
                    if activeWindow == 0 and targetInventory == ExitIndex:
                        break
                    elif activeWindow == 1 and targetShop == ExitIndex:
                        break
                    elif activeWindow == 0 and targetItem != None:
                        if self.player.SellItem(targetItem):
                            shopItems = targetItem.AddToInventory(shopItems)
                    elif activeWindow == 1 and targetItem != None:
                        if self.player.BuyItem(targetItem):
                            shopItems = targetItem.RemoveFromInventory(shopItems)
                case Key.KEY_ESC:
                    break
        self.update_layout("MainTop",visible=False)

    def TawernScreen(self):
        menus = [self.rest]
        options = ["Rest (5 Coins)","Back"]
        target = 0
        while True:
            InfoScreen = self.OptionsToText(options,target)
            DescriptionScreen = self.player.PrintStats()
            self.update_layout("TopL",InfoScreen,f"{self.player.Coins} Coins",ratio=1)
            self.update_layout("TopR",DescriptionScreen,self.player.Name,ratio=1)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1: return
                    else: menus[target]()
                case Key.KEY_ESC:
                    return

    def rest(self):
        if self.player.Coins < 5: return
        self.player.Coins -= 5
        text = Text("You feel rested\n\n")
        for name,value in self.player.Statistics.items():
            if name[0:3] != "Max": continue
            if self.player.Statistics[name[3:len(name)]] >= value: continue
            self.player.Statistics[name[3:len(name)]] = value
            text.append(f"Your {name[3:len(name)]} is restored\n")
        text.append("\nPress any key to continue")
        self.update_layout("TopL","You are resting",ratio=1)
        sleep(0.4)
        self.update_layout("TopL","You are resting.",ratio=1)
        sleep(0.4)
        self.update_layout("TopL","You are resting..",ratio=1)
        sleep(0.4)
        self.update_layout("TopL","You are resting...",ratio=1)
        sleep(0.4)
        self.update_layout("TopL",text,ratio=1)
        self.update_layout("TopR",self.player.PrintStats(),self.player.Name,ratio=1)
        self.Tick()
        Key.get_input()

    def LoadScreen(self):
        targetSaveOption = 0
        SaveOptions = ['Load','Menu','Delete']
        target = 0
        while True:
            saves = []
            for file in os.listdir(SaveFilePath):
                filename = os.fsdecode(file)
                if filename.endswith(".json"): 
                    saves.append(filename.split(".json")[0])
            if saves == []: return self.NewGameScreen()
            SaveListText = Text(justify="right")
            SaveOptionText = Text()

            for index,saveName in enumerate(saves):
                if target == index:
                    SaveListText.append(f">{saveName}\n",style=f"{HIGHLIGHT_COLOR}")
                    for optionIndex,option in enumerate(SaveOptions):
                        if targetSaveOption == len(SaveOptions)-1 and optionIndex == targetSaveOption:
                             SaveOptionText.append(f"{option}",style=f"u {DANGER_COLOR}")
                        elif targetSaveOption == optionIndex:
                            SaveOptionText.append(f"{option}",style=f"u {HIGHLIGHT_COLOR}")
                        else:
                            SaveOptionText.append(f"{option}",style=f"{TEXT_COLOR}")
                        SaveOptionText.append(" ",style=None)
                    SaveOptionText.append("\n")
                    data = {}
                    with open(SaveFilePath+"/"+saveName+".json", "r") as read_file:
                        data = json.load(read_file)
                        read_file.close()
                    SaveOptionText.append(f"{data['Name']}\n")
                    SaveOptionText.append(f"Class: {data['Statistics']['Class']}\nLevel: {data['Statistics']['Level']}\nTurn-{data['tick']}\n")
                else:
                    SaveOptionText.append("\n")
                    SaveListText.append(f"{saveName}\n",style=f"{TEXT_COLOR}")

            self.update_layout("TopL",SaveListText,"Saves",ratio=1)
            self.update_layout("TopR",SaveOptionText,"Actions",ratio=1)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=1)
            oldTarget = target
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(saves)-1: target = 0
                    if oldTarget != target: targetSaveOption = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(saves)-1
                    if oldTarget != target: targetSaveOption = 0
                case Key.KEY_a | Key.KEY_Aleft :
                    targetSaveOption -= 1
                    if targetSaveOption < 0 : targetSaveOption = 0
                case Key.KEY_d | Key.KEY_Aright :
                    targetSaveOption += 1
                    if targetSaveOption > 2: targetSaveOption = 2
                case Key.KEY_enter | Key.KEY_space:
                    match targetSaveOption:
                        case 0:
                            if self.LoadGame(saves[target]) == True: return True
                        case 1:
                            return
                        case 2:
                            self.DeleteSaveScreen(saves[target])
                case Key.KEY_ESC:
                    return

    def DeleteSaveScreen(self,SaveName:str):
        while True:
            fileText = Text(f"\n\nDo you really want to remove save file\n'{SaveName}'",justify="center")
            text = Text("Press ANY other key to cancel", justify='center')
            self.update_layout("TopL","",ratio=1)
            self.update_layout("TopR",fileText,ratio=1)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR",text,title="Press Y key to delete",ratio=3)
            self.update_layout("Left",ratio=0)
            self.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_y:
                    os.remove(f"{SaveFilePath}/{SaveName}.json")
                    return
                case _:
                    return

    def LoadGame(self,SaveName:str):
        # CurrentSaveFileName = SaveName.split(".json")[0]
        data = {}
        with open(SaveFilePath+"/"+SaveName+".json", "r") as read_file:
            data = json.load(read_file)
            read_file.close()

        if data['GameVersion'] != GameVersion:
            while True:
                SaveVersionText = Text(f"Save version\n{data['GameVersion']}",justify="right")
                GameVersionText = Text(f"Game version\n{GameVersion}")
                text = Text("\n\nSave version is different from Game version\n",justify='center')
                text.append("Press Y key to continue\n")
                self.update_layout("TopL",SaveVersionText,ratio=1)
                self.update_layout("TopR",GameVersionText,ratio=1)
                self.update_layout("MainTop",text)
                if Key.get_input() != Key.KEY_y:
                    self.update_layout("MainTop",visible=False)
                    return False
                else: break

        self.update_layout("MainTop",visible=False)

        self.player.Name = data['Name']
        for SaveStat in data['Statistics']:
            if SaveStat in self.player.Statistics:
                self.player.Statistics[SaveStat] = data['Statistics'][SaveStat]
        for bonus in data['Bonuses']:
            self.player.Bonuses[bonus] = data['Bonuses'][bonus]
        for item in data['Inventory']:
            if data['Inventory'][item] == None: continue
            self.player.Inventory.append(ItemClass.DictionaryToItem(data['Inventory'][item]))
        for Slot in data['Equipment']:
            if data['Equipment'][Slot] == None:
                self.player.Equipment[Slot] == None
                continue
            self.player.Equipment[Slot] = ItemClass.DictionaryToItem(data['Equipment'][Slot])
        for content in data['Location']:
            self.player.Location[content] = data['Location'][content]
        self.player.tick = data['tick']
        self.player.tickGameUpdate = data['tickGameUpdate']
        try:
            pass
        except:
            pass
        
        return True
        
    def ContinueSave(self):
        pass

    def SaveGame(self,SaveName:str):
        Save = {
            'Name' : self.player.Name,
            'Statistics' : {},
            'Bonuses': {},
            'Inventory' : {},
            'Equipment' : {},
            'Location' : {},
            'GameVersion': GameVersion,
            'tick': self.player.tick,
            'tickGameUpdate': self.player.tickGameUpdate,
        }
        for stat in self.player.Statistics:
            Save['Statistics'][stat] = self.player.Statistics[stat]
        for bonus in self.player.Bonuses:
            Save['Bonuses'][bonus] = self.player.Bonuses[bonus]
        for item in self.player.Inventory:
            Save['Inventory'][id(item)] = item.ItemToDictionary()
        for slot in self.player.Equipment:
            if self.player.Equipment[slot] == None:
                Save["Equipment"][slot] = None
                continue
            Save["Equipment"][slot] = self.player.Equipment[slot].ItemToDictionary()
        for content in self.player.Location:
            Save['Location'][content] = self.player.Location[content]
        
        with open(SaveFilePath+"/"+SaveName +".json", "w") as write_file:
            json.dump(Save, write_file)
            write_file.close()
        # CurrentSaveFileName = SaveName

    def SaveScreen(self):
        target = 0
        while True:
            saves = ['New Save File']
            for file in os.listdir(SaveFilePath):
                filename = os.fsdecode(file)
                if filename.endswith(".json"): 
                    saves.append(filename.split(".json")[0])
            if saves == []: return self.NewGameScreen()
            SaveListText = Text()

            for index,saveName in enumerate(saves):
                if target == 0 and index == 0:
                    SaveListText.append(f">{saveName}\n",style=f"{NEW_SAVE_FILE}")
                elif target == index:
                    SaveListText.append(f">{saveName}\n",style=f"{HIGHLIGHT_COLOR}")
                else:
                    SaveListText.append(f"{saveName}\n",style=f"{TEXT_COLOR}")

            self.update_layout("TopL","",ratio=1)
            self.update_layout("TopR",SaveListText,ratio=1)
            self.update_layout("BottomL","",ratio=0)
            self.update_layout("BottomR","",ratio=0)
            self.update_layout("Left",ratio=1)
            self.update_layout("Right",ratio=2)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(saves)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(saves)-1
                case Key.KEY_enter | Key.KEY_space:
                    if target == 0:
                        if self.NewSaveScreen() == True: break
                    else:
                        self.SaveGame(saves[target])
                        break
                case Key.KEY_ESC:
                    break

    def NewSaveScreen(self):
        userSaveName = ""
        while True:
            text = Text("\n",justify='center')
            text.append(f"{userSaveName}" if userSaveName != "" else f"'{self.player.Name}'")
            self.update_layout("MainTop",text,"Save file name:",ratio=2)
            userInput = msvcrt.getwch()
            if userInput == '\r':
                if userSaveName == "":
                    userSaveName = self.player.Name
                if os.path.exists(f"{SaveFilePath}/{userSaveName}.json"):
                    overwriteText = Text("Save file already exists\n",justify='center')
                    overwriteText.append(f"{userSaveName}\n",style=f"{DANGER_COLOR}")
                    overwriteText.append(f"Press Y to overwrite\n")
                    if self.ConfirmScreen(overwriteText):
                        self.SaveGame(userSaveName)
                        self.update_layout("MainTop",visible=False)
                        return True
                    else:
                        break
                self.SaveGame(userSaveName)
                self.update_layout("MainTop",visible=False)
                return True
            elif userInput == '\x1b':
                break
            elif userInput == '\x08':
                userSaveName = userSaveName[:-1]
            elif userInput == '\t' or userInput == '\x00':
                pass
            elif len(userSaveName) < 22:
                userSaveName += str(userInput)
        self.update_layout("MainTop",visible=False)

    player = Player()

    def run(self):
        try:
            with open("Settings.json", "r") as read_file:
                self.Settings = json.load(read_file)
                read_file.close()
        except:
            pass
        FontSize.run(self.Settings['FontSize'])
        GameState.State = GameState.LOADED
        with Live(layout,refresh_per_second=60,screen=True) as live:
            # self.disable_window_resize()
            # self.disable_quickedit()
            self.StartScreen()
                
game = Game()

class Tiles:
    def __init__(self,Name:str="Town",MapSymbol:str="#",MapColor:str="white",Hostile:bool=False,PossibleEnemies=[],**Contents):
        self.Name = Name
        self.MapSymbol = MapSymbol
        self.MapColor = MapColor
        self.Hostile = Hostile
        self.PossibleEnemies = PossibleEnemies
        self.Content = {}
        for name,value in Contents.items():
            self.Content[name] = value

    
    def DisplayTileInfo(self):
        text = Text()
        text.append(f"{self.Name}\n")
        if self.Hostile: text.append("Hostile\n",style="red")
        if self.Content != {}: text.append("Activities:\n")
        for name, _ in self.Content.items():
            text.append(f"*{name}\n")
        return text

ForestTile = Tiles("Forest","T","green",False,[Dummy],Fight=game.FightScreen)
DenceForestTile = Tiles("Dence Forest","D","dark_green",True,[Dummy,Bandit],Fight=game.FightScreen)
TownTile = Tiles("Town","█","royal_blue1",False,Tawern=game.TawernScreen,Shop=game.ShopScreen)
RoadTile = Tiles("Road","#","grey53",False,[Bandit])
VillageTile = Tiles("Village","█","orange4",False,Tawern=game.TawernScreen)
GameTileBase = [ForestTile,DenceForestTile,RoadTile,TownTile,VillageTile]

class GameMap:
    GameMap = []
    def __init__(self,DisplayWidth:int=51,DisplayHeight:int=21):
        GameMapFile = []
        with open("GameMap.map", "rb") as write_file:
            GameMapFile = pickle.load(write_file)
            write_file.close()
        self.GenerateMap(GameMapFile)
        self.Height = len(self.GameMap)
        self.Width = len(self.GameMap[0])
        self.DisplayWidth = DisplayWidth
        self.DisplayHeight = DisplayHeight
        if self.DisplayWidth == None: self.DisplayWidth = self.Width
        if self.DisplayHeight == None: self.DisplayHeight = self.Height

    def GenerateMap(self,MapFile):
        for height in range(len(MapFile[0])):
            self.GameMap.append([])
            for width in range(len(MapFile)):
                self.GameMap[height].append(GameTileBase[MapFile[width][height]])

    def DisplayMap(self,PlayerPosition):
        text = Text()
        x_range = range(self.DisplayWidth)
        y_range = range(self.DisplayHeight)
        # X MAP DISPLAY LIMIT 
        if PlayerPosition[0]-floor(self.DisplayWidth/2) > 0:
            x_range = range(PlayerPosition[0]-floor(self.DisplayWidth/2),PlayerPosition[0]+ceil(self.DisplayWidth/2))
        if PlayerPosition[0]+ceil(self.DisplayWidth/2) > self.Width:
            x_range = range(self.Width-self.DisplayWidth,self.Width)
        # Y MAP DISPLAY LIMIT 
        if PlayerPosition[1]-floor(self.DisplayHeight/2) > 0:
            y_range = range(PlayerPosition[1]-floor(self.DisplayHeight/2),PlayerPosition[1]+ceil(self.DisplayHeight/2))
        if PlayerPosition[1]+ceil(self.DisplayHeight/2) > self.Height:
            y_range = range(self.Height-self.DisplayHeight,self.Height)
        
        for y in y_range:
            for x in x_range:
                Tile = self.GameMap[y][x]
                if PlayerPosition[0] == x and PlayerPosition[1] == y:
                    text.append("@")
                    continue
                text.append(f"{Tile.MapSymbol}",style=f"{Tile.MapColor}")
            text.append("\n")
        return text

    def GetTile(self,Position):
        return self.GameMap[Position[1]][Position[0]]
Map = GameMap()



if __name__ == "__main__":
    game.set_window("Rpg game", 55, 30)
    game.run()