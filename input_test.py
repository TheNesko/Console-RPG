import msvcrt, random
from copy import deepcopy as copy
from typing import Any

# for x in range(100):
#     ky = msvcrt.getch()
#     print(ky)
#     if ky in [b'\x00', b'\xe0']:
#         ky = msvcrt.getch()
#         print(ky)
#         print(ord(ky))
#     else:
#         print(ord(ky.lower()))



#==========ITEM=COPYING===========#
# class Item:
#     def __init__(self,Name,**Statistics) -> None:
#         self.Name = Name
#         self.id = hash(self.Name)
#         self.Statistics = {}
#         for name,value in Statistics.items():
#             self.Statistics[name] = value


# Sword = Item("Sword",Attack=100)
# Sword2 = copy(Sword)
# Sword2.Statistics['Attack'] = 10

# ItemList = [Sword,Sword2]

# for x in ItemList:
#     print(f"{id(x)} - {x.Name} - {x.Statistics}")
# print(Sword.id==Sword2.id)
# print(Sword==Sword2)
#=================================#


#==========ENUMS=CLASSES===========#
# class Potion:
#     class Effect:
#         RESTORE = 'Restore'
#         HEAL = 'Heal'
#
#     def __init__(self,Effect=None) -> None:
#         self.Effect = Effect
#
# test = Potion(Potion.Effect.RESTORE)
# print(test.Effect)
#=================================#


# ==========COMBAT=TESTING==========#
# class Fight:
#     CritHits = 0
#     DealtDamage = 0
#     def __init__(self,MaxHealth:int,Attack:int,Armor:int,ArmorPen:float,CritRate:float,CritDamage:float,**ScaledStats):
#         self.Statistics = {
#             'Level' : 1,
#             'MaxHealth' : MaxHealth,
#             'Health' : MaxHealth,
#             'Attack' : Attack,
#             'Armor' : Armor,
#             'ArmorPenetraion': ArmorPen,
#             'CritRate' : CritRate,
#             'CritDamage' : CritDamage,
#         }
    
#     @property
#     def Health(self):
#         return self.Statistics['Health']
    
#     @Health.setter
#     def Health(self,value):
#         self.Statistics['Health'] = value
#         if self.Statistics['Health'] > self.Statistics['MaxHealth']:
#             self.Statistics['Health'] = self.Statistics['MaxHealth']
#         elif self.Statistics['Health'] < 0:
#             self.Statistics['Health'] = 0

#     def CalculateDamage(self,Attack:int,Armor:int,ArmorPen:float):
#         Armor -= Armor*ArmorPen
#         reduction = 1+Armor/100
#         result = Attack/reduction
#         return int(result)
    
#     def Damage(self,Enemy):
#         Attack = self.Statistics['Attack']
#         ArmorPen = self.Statistics['ArmorPenetraion']
#         CritRate = self.Statistics['CritRate']*100
#         CritDamage = self.Statistics['CritDamage']
#         EnemyArmor = Enemy.Statistics['Armor']
#         Damage = self.CalculateDamage(Attack,EnemyArmor,ArmorPen)
#         CritRoll = random.randrange(0,100)
#         if CritRoll < CritRate:
#             # CRITICAL HIT
#             self.CritHits += 1
#             Damage = int(Damage * CritDamage)
#         self.DealtDamage += Damage
#         return Damage

# class Enemy(Fight):
#     def __init__(self, MaxHealth: int, Attack: int, Armor: int, ArmorPen: float, CritRate: float, CritDamage: float, **ScaledStats):
#         super().__init__(MaxHealth, Attack, Armor, ArmorPen, CritRate, CritDamage, **ScaledStats)

# class Player(Fight):
#     def __init__(self, MaxHealth: int, Attack: int, Armor: int, ArmorPen: float, CritRate: float, CritDamage: float, **ScaledStats):
#         super().__init__(MaxHealth, Attack, Armor, ArmorPen, CritRate, CritDamage, **ScaledStats)

# TestEnemy = Enemy(100,10,50,0.08,0.15,1.5)
# TestPlayer = Player(100,10,50,0.08,0.15,1.5)

# x = 10000
# for turn in range(x):
#     TestPlayer.Damage(TestEnemy)
    # if TestEnemy.Health == 0:
    #     print(f"Killed Enemy on turn {turn}")
    #     print(f"{TestPlayer.CritHits}/{turn} Critical hits = CritRate:{(TestPlayer.CritHits/turn)*100}%")
    #     print(f"{TestPlayer.DealtDamage/turn} Average Damage dealt")
    #     break

# print(f"{TestPlayer.CritHits}/{x} Critical hits = CritRate:{(TestPlayer.CritHits/x)*100}%")
# print(f"{TestPlayer.DealtDamage/x} Average Damage dealt")
# =================================#


class Test:
    Level = 1
    Exp = 0
    NeedExp = 100

    def SetExp(self,value):
            self.Exp = value
            if self.Exp >= self.NeedExp:
                if self.Level >= 100:
                     self.Exp = self.NeedExp
                     return
                self.Level += 1
                overflow = self.Exp - self.NeedExp
                self.Exp = 0
                self.NeedExp = round((self.Level-1)**3+100)
                print(f"Level {self.Level} Exp {self.Exp}/{self.NeedExp}")
                self.SetExp(overflow)

test = Test()
while True:
    msvcrt.getch()
    test.SetExp(test.Exp+100000)