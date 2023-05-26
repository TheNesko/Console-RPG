from imports import *
from characters import Character

class ItemClass:
    item_list = []

    def __init__(self,name:str="404Error",**Stats):
        ItemClass.item_list.append(self)
        self._Name = name
        self.id = hash(self._Name)
        self.Sellable = True
        self.stats = {}
        for Stat,value in Stats.items():
            self.stats[Stat] = value

    @property
    def name(self):
        return self._Name
    
    @name.setter
    def name(self,value):
        self._Name = value

    def PrintStats(self,text):
        for stat in self.stats:
            if self.stats[stat] == None: continue
            if type(self.stats[stat]) == float:
                text.append(f"{stat}: {round(self.stats[stat]*100)}%\n")
            elif type(self.stats[stat]) == int:
                text.append(f"{stat}: {self.stats[stat]}\n")
            elif type(self.stats[stat]) == str:
                text.append(f"{self.stats[stat]}\n")
            elif type(self.stats[stat]) == type([]):
                text.append(f"{stat}: \n")
                for x in self.stats[stat]:
                    text.append(f"  *{x}\n")
        return text
    
    def getTypeName(self):
        return self.__class__.__name__

    def ItemToDictionary(self):
        Item = {
            'name': self._Name,
            'stats': {}
        }
        for stat in self.stats:
            Item['stats'][stat] = self.stats[stat] 
        return Item

    @staticmethod
    def DictionaryToItem(dict):
        newItem = None
        match dict['Type']:
            case Equipment.__name__:
                newItem = Equipment(dict['name'],dict['Price'],dict['Slot'],dict['Class'])
            case Potion.__name__:
                newItem = Potion(dict['name'],dict['Price'],dict['Effect'])
            case Resource.__name__:
                newItem = Resource(dict['name'],dict['BasePrice'],dict['Ammount'])
            case Currency.__name__:
                newItem = Currency(dict['name'],dict['BasePrice'],dict['Ammount'])
        for stat in dict['stats']:
            newItem.stats[stat] = dict['stats'][stat]
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

    def __init__(self, name: str = "404Error",Price:int=1,Slot:str=Slot.PRIMARY,Class:str=None, **Stats):
        super().__init__(name, **Stats)
        self.Price = Price
        self.Slot = Slot
        self.Class = Class
    
    def PrintStats(self):
        text = Text()
        text.append(f"{self.name}\nPrice {self.Price}\nSlot: {self.Slot}\n")
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
            'name': self._Name,
            'Type': self.getTypeName(),
            'Price': self.Price,
            'Slot': self.Slot,
            'Class': self.Class,
            'stats': {}
        }
        for stat in self.stats:
            Item['stats'][stat] = self.stats[stat] 
        return Item

    def Use(self, player):
        return player.EquipItem(self)


class Potion(ItemClass):
    class Effect:
        RESTORE = 'Restore'

    def __init__(self, name: str = "404Error",Price:int=1,Effect:str=Effect.RESTORE, **Stats):
        super().__init__(name, **Stats)
        self.Price = Price
        self.Effect = Effect

    def PrintStats(self):
        text = Text()
        text.append(f"{self.name}\nPrice: {self.Price}\n{self.Effect}\n")
        return super().PrintStats(text)
    
    def ItemToDictionary(self):
        Item = {
            'name': self._Name,
            'Type': self.getTypeName(),
            'Price': self.Price,
            'Effect': self.Effect,
            'stats': {}
        }
        for stat in self.stats:
            Item['stats'][stat] = self.stats[stat] 
        return Item
    
    def Use(self, player):
        return player.ConsumeItem(self)


class Resource(ItemClass):
    def __init__(self, name: str = "404Error",BasePrice:int=1,Ammount:int=1, **Stats):
        super().__init__(name, **Stats)
        self.BasePrice = BasePrice
        self.Ammount = Ammount
        self._Price = self.BasePrice * self.Ammount

    @property
    def Price(self):
        return self.BasePrice * self.Ammount
    
    @property
    def name(self):
        if self.Ammount > 1: return f"{self._Name}s"
        return self._Name

    def PrintStats(self):
        text = Text()
        text.append(f"{self.name}\nPrice: {self.BasePrice}\nFull Price: {self.Price}\nAmmount: {self.Ammount}")
        return super().PrintStats(text)

    def ItemToDictionary(self):
        Item = {
            'name': self._Name,
            'Type': self.getTypeName(),
            'BasePrice': self.BasePrice,
            'Ammount': self.Ammount,
            'stats': {}
        }
        for stat in self.stats:
            Item['stats'][stat] = self.stats[stat] 
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


class Currency(Resource):
    def __init__(self, name: str = "404Error", BasePrice: int = 1, Ammount: int = 1, **Stats):
        super().__init__(name, BasePrice, Ammount, **Stats)
        self.Sellable = False
    
    def PrintStats(self):
        text = Text()
        text.append(f"{self.name}\nAmmount: {self.Ammount}")
        return text


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
            text.append(f"{ammount}x {item.name}\n" if ammount > 1 else f"{item.name}\n")
        if LootAmmount == 0: return False
        return text


class ItemDataBase:
    #ALL CLASSES
    leather_armor = Equipment("Leather Armor",70,Equipment.Slot.ARMOR,None,Armor=10)
    iron_dagger = Equipment("Iron Dagger",10,Equipment.Slot.SECONDARY,None,Attack=7,CritDamage=0.1)
    #WARRIOR
    steel_sword = Equipment("Steel Sword",275,Equipment.Slot.PRIMARY,Character.WARRIOR,Attack=12,CritDamage=0.05)
    iron_armor = Equipment("Iron Armor",300,Equipment.Slot.ARMOR,Character.WARRIOR,Armor=25,MaxStamina=-5)
    round_shield = Equipment("Round Shield",100,Equipment.Slot.SECONDARY,Character.WARRIOR,Armor=25,CritRate=-0.03,CritDamage=0.1)
    #MAGE
    wizzard_hat = Equipment("Wizzard Hat",50,Equipment.Slot.HELMET,None,Armor=5,MaxMana=10)
    indel_staff = Equipment("Indel's Staff",2500,Equipment.Slot.PRIMARY,Character.MAGE,Attack=20,CritDamage=0.2,CritRate=0.05)
    begginers_wand = Equipment("Begginer's Wand",40,Equipment.Slot.PRIMARY,Character.MAGE,Attack=5,ArmorPenetration=0.05)
    mystic_orb = Equipment("Mystic Orb",150,Equipment.Slot.SECONDARY,Character.MAGE,Attack=3,ArmorPenetration=0.08,CritRate=-0.03)
    mage_student_cloak = Equipment("Mage Student's Cloak",100,Equipment.Slot.ARMOR,Character.MAGE,Armor=10,MaxMana=20)
    #RANGER
    elven_shortbow = Equipment("Elven Shortbow",250,Equipment.Slot.PRIMARY,Character.RANGER,Attack=5,CritRate=0.1)

    #POTIONS
    health_restore = Potion("Health restore",5,Potion.Effect.RESTORE,Health=0.3)
    weak_mana_restore = Potion("Weak Mana restore",5,Potion.Effect.RESTORE,Mana=25)
    mana_restore = Potion("Mana restore",10,Potion.Effect.RESTORE,Mana=0.5)
    stat_restore = Potion("Angel's kiss",29,Potion.Effect.RESTORE,Health=1.0,Stamina=1.0,Mana=1.0)

    #RESOURCES
    log = Resource("Log",1)
    stone = Resource("Stone",2)
    iron_ore = Resource("Iron ore", 4)
    iron_bar = Resource("Iron bar", 12)

    #CURRENCY
    coin = Currency("Coin")
