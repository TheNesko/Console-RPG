from imports import *
from input import Key
from display import layout, Display, Color, Ascii
from characters import Player
from characters import Character
from game_map import Map
from game_map import TileDataBase as tileDB
from items import ItemDataBase as itemDB
from save import SAVE_FILE_PATH

class GameState:
    STARTING = 0
    LOADED = 1
    State = STARTING

class Game:
    player = Player()
    game_map = Map()

    def run(self):
        try:
            with open("settings.json", "r") as read_file:
                self.settings = json.load(read_file)
                read_file.close()
        except:
            pass
        FontSize.run(self.settings['FontSize'])
        GameState.State = GameState.LOADED
        with Live(layout,refresh_per_second=60,screen=True) as live:
            # self.disable_window_resize()
            # self.disable_quickedit()
            self.start_screen()

    def Tick(self):
        self.player.tick += 1
        if self.player.tick >= self.player.tick_game_update:
            self.player.tick_game_update = self.player.tick + random.randint(7, 14)
            # DO GAME UPDATES
            self.generate_shop_items()

    def confirm_screen(self, text:Text):
        Display.active_layout(Display.CONFIRM)
        Display.update_layout(Display.CONFIRM, "main", text)
        if Key.get_input() == Key.KEY_y:
            return True
        return False

    def start_screen(self):
        menus = [self.play_screen, self.settings_screen, self.credits_screen]
        options = ["Play", "Options", "Credits", "Exit"]
        target = 0
        while True:
            game_name = Ascii.game_name()
            option_screen = Display.options_to_text(options,target)

            Display.active_layout(Display.MENU)
            Display.update_layout(Display.MENU, "top", game_name, ratio=2)
            Display.update_layout(Display.MENU, "bottom", option_screen, ratio=6)

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
    
    settings = {'FontSize':22,'CombatSpeed':1}
    def settings_screen(self):
        options = []
        for name in self.settings:
            options.append(name)
        options.append("Back")
        target = 0
        while True:
            option_screen = Text("\n\n",justify="center")
            
            for index,name in enumerate(options):
                if index == len(options)-1 and target == index:
                    option_screen.append(f"{name}\n",style=f"u {Color.GO_BACK_COLOR}")
                elif index == target:
                    option_screen.append(f"<- - {name} [{self.settings[name]}] + ->\n", style=f"u {Color.HIGHLIGHT_COLOR}")
                elif index == len(options)-1:
                    option_screen.append(f"{name}\n", style=f"{Color.TEXT_COLOR}")
                else:
                    option_screen.append(f"{name} [{self.settings[name]}]\n", style=f"{Color.TEXT_COLOR}")

            Display.active_layout(Display.MENU)
            Display.update_layout(Display.MENU, "top", ratio=0)
            Display.update_layout(Display.MENU, "bottom", option_screen, ratio=1)

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
                            self.settings['FontSize'] = FontSize.getFontSize()
                        case 1:
                            self.settings['CombatSpeed'] = max(self.settings['CombatSpeed']-1,1)
                case Key.KEY_Aright | Key.KEY_d:
                    match target:
                        case 0:
                            FontSize.run(min(FontSize.getFontSize()+1,30))
                            self.settings['FontSize'] = FontSize.getFontSize()
                        case 1:
                            self.settings['CombatSpeed'] = min(self.settings['CombatSpeed']+1,5)
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1: break
                case Key.KEY_ESC:
                    break
        with open("settings.json", "w") as write_file:
            json.dump(self.settings, write_file)
            write_file.close()

    def credits_screen(self):
        text = [
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
            ascii_text = Ascii.credits()
            credits_text = Text(justify="center")
            for index in range(target, len(text)):
                credits_text.append(f"{text[index]}\n", Color.TEXT_COLOR)

            Display.active_layout(Display.MENU)
            Display.update_layout(Display.MENU, "top", ascii_text, ratio=2)
            Display.update_layout(Display.MENU, "bottom", credits_text, ratio=6)

            # Display.update_layout("TopL", ascii_text, ratio=2)
            # Display.update_layout("TopR", ratio=1)
            # Display.update_layout("BottomL", credits_text, "press ESC to exit", ratio=6)
            # Display.update_layout("BottomR", ratio=1)
            # Display.update_layout("Left", ratio=1)
            # Display.update_layout("Right", ratio=0)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(text)-1: target = len(text)-1
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = 0
                case Key.KEY_ESC | Key.KEY_enter | Key.KEY_space:
                    return
    
    def play_screen(self):
        menus = [self.NewGameScreen,self.ContinueSave,self.LoadScreen]
        options = ["New game","Continue","Load","Back"]
        target = 0
        while True:
            match target:
                case 0:
                    ascii_text = Ascii.new_game()
                case 1 | 2:
                    ascii_text = Ascii.load()
                case 3:
                    ascii_text = Ascii.back()
            option_screen = Display.options_to_text(options,target)

            Display.active_layout(Display.MENU)
            Display.update_layout(Display.MENU, "top", ascii_text, ratio=2)
            Display.update_layout(Display.MENU, "bottom", option_screen, ratio=6)
            
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
        for x in Character.character_list:
            options.append(x.name)
        options.append("Back")
        target = 0
        while True:
            info_screen = Display.options_to_text(options,target)
            if target <= len(Character.character_list)-1:
                CharactersDescriptions = Character.character_list[target].print_stats()
            else:
                CharactersDescriptions = Ascii.back()
            Display.update_layout("TopL",info_screen,ratio=2)
            Display.update_layout("TopR",CharactersDescriptions,ratio=2)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=2)
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
                        self.player.NewCharacter(Character.character_list[target])
                        if self.NameCharacterScreen(): return
                        return True
                case Key.KEY_ESC:
                    return

    def NameCharacterScreen(self):
        PlayerName = ""
        while True:
            NamingScreen = Text(f"\nName your character\n",justify="center")
            NamingScreen.append(f"{PlayerName}" if PlayerName != "" else f"'{self.player.name}'")
            Display.update_layout("TopL",ratio=2)
            Display.update_layout("TopR","",ratio=0)
            Display.update_layout("BottomL",NamingScreen,f"You choose {self.player.stats['Class']}",ratio=6)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=0)
            userInput = msvcrt.getwch()
            if userInput == '\r':
                if PlayerName != "":
                    self.player.name = PlayerName
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
            info_screen = Display.options_to_text(options,target)
            DescriptionScreen = self.player.print_stats()
            Display.update_layout("TopL",info_screen,f"Location: {self.game_map.get_tile(self.player.get_position()).name}",ratio=1)
            Display.update_layout("TopR",DescriptionScreen,self.player.name,ratio=1)
            Display.update_layout("BottomL","",ratio=1)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
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
            tileInfo = self.game_map.get_tile(self.player.get_position()).DisplayTileInfo()
            mapScreen = self.game_map.DisplayMap(self.player.get_position())
            mapScreen.justify = "center"
            mapLegend = Text()
            for tile in tileDB.__dict__:
                mapLegend.append(f"{tile.MapSymbol}",style=f"{tile.MapColor}")
                mapLegend.append(f" - {tile.name}\n")
            Display.update_layout("TopL",tileInfo,"Tile info",ratio=1)
            Display.update_layout("TopR",mapLegend,"Legend",ratio=1)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
            Display.update_layout("Map",mapScreen,"Map",border=box.ASCII2)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    self.player.Location['y'] += 1
                    if self.player.Location['y'] > self.game_map.Height-1:self.player.Location['y'] = self.game_map.Height-1
                    else: self.Tick()
                case Key.KEY_Aup | Key.KEY_w:
                    self.player.Location['y'] -= 1
                    if self.player.Location['y'] < 0: self.player.Location['y'] = 0
                    else: self.Tick()
                case Key.KEY_Aright | Key.KEY_d:
                    self.player.Location['x'] += 1
                    if self.player.Location['x'] > self.game_map.Width-1: self.player.Location['x'] = self.game_map.Width-1
                    else: self.Tick()
                case Key.KEY_Aleft | Key.KEY_a:
                    self.player.Location['x'] -= 1
                    if self.player.Location['x'] < 0: self.player.Location['x'] = 0
                    else: self.Tick()
                case Key.KEY_enter | Key.KEY_space:
                    if self.ActivityScreen():
                        Display.update_layout("Map",visible=False)
                        return True
                case Key.KEY_ESC | Key.KEY_tab:
                    break
        Display.update_layout("Map",visible=False)

    def ActivityScreen(self):
        map_tile = self.game_map.get_tile(self.player.get_position())
        if map_tile.Content == {}: return
        target = 0
        while True:
            menus = []
            options = []
            for name,value in map_tile.Content.items():
                if type(value) == bool: continue
                menus.append(value)
                options.append(name)
            if menus == []: return
            options.append("Back")
            optionsText = Display.options_to_text(options,target)
            Display.update_layout("TopL",optionsText,"Activities",ratio=1)
            Display.update_layout("TopR",ratio=0)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
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
        Display.update_layout("Map",visible=False)

    def FightScreen(self):
        self.layoutToggleVisible("Map",True)
        map_tile = self.game_map.get_tile(self.player.get_position())
        Enemy = None
        EnemyFindRoll = 0.4
        if map_tile.Hostile == True: EnemyFindRoll = 0.8
        if (EnemyFindRoll*100) > random.randrange(0,100) and map_tile.enemies != []:
            Enemy = copy(map_tile.enemies[random.randint(0,len(map_tile.enemies)-1)])
        if Enemy == None:
            text = Text("\n\nThere are no enemies around",justify='center',style=Color.DANGER_COLOR)
            Display.update_layout("TopL",text,"Press any key to continue",ratio=1)
            Display.update_layout("Right",ratio=0)
            self.Tick()
            Key.get_input()
            return
        target = 0
        options = [Enemy.name,"Back"]
        while True:
            text = Display.options_to_text(options,target)
            Display.update_layout("TopL",text,ratio=1)
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
    
    def CombatScreen(self,Enemy):
        target = 0
        while True:
            options = []
            for ability in self.player.abilities:
                options.append(ability.name)
            options.append("Inventory")
            options.append("Escape")
            
            options_text = Text()
            for index,option in enumerate(options):
                if index == len(options)-1 and target == index:
                    options_text.append(f">{index+1}.{option}\n",f"u {Color.GO_BACK_COLOR}")
                elif index == target:
                    if index < len(options)-2:
                        if self.player.abilities[index].can_use(self.player):
                            options_text.append(f">{index+1}.{option}\n",f"u {Color.HIGHLIGHT_COLOR}")
                        else:
                            options_text.append(f">{index+1}.{option}\n",f"u {Color.UNAVALIBLE}")
                    else:
                        options_text.append(f">{index+1}.{option}\n",f"u {Color.HIGHLIGHT_COLOR}")
                else:
                    if index < len(options)-2:
                        if self.player.abilities[index].can_use(self.player):
                            options_text.append(f"{index+1}.{option}\n",Color.TEXT_COLOR)
                        else:
                            options_text.append(f"{index+1}.{option}\n",Color.UNAVALIBLE)
                    else:
                        options_text.append(f"{index+1}.{option}\n",Color.TEXT_COLOR)
            
            ability_stats_text = Text()
            if target < len(options)-2:
                ability_stats_text = self.player.abilities[target].print_stats(self.player)
            Display.update_layout("MainTop",ratio=0)
            Display.update_layout("TopL",options_text,"Actions",ratio=3)
            Display.update_layout("TopR",ability_stats_text,ratio=3)
            Display.update_layout("BottomL",self.player.print_combat_stats(),self.player.name,ratio=6)
            Display.update_layout("BottomR",Enemy.print_combat_stats(),Enemy.name,ratio=6)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_Adown | Key.KEY_s:
                    target += 1
                    if target > len(options)-1: target = 0
                case Key.KEY_Aup | Key.KEY_w:
                    target -= 1
                    if target < 0: target = len(options)-1
                case Key.KEY_enter | Key.KEY_space:
                    if target == len(options)-1:
                        break
                    elif target == len(options)-2:
                        Display.update_layout("MainTop",ratio=0)
                        self.InventoryScreen()
                    else:
                        Display.update_layout("TopL",ratio=0)
                        Display.update_layout("TopR",ratio=0)
                        # PLAYER TURN
                        if self.player.abilities[target].can_use(self.player) == False:
                            continue
                        combat_text = self.player.abilities[target].use(self.player,Enemy)
                        Display.update_layout("MainTop",combat_text,"Combat in progress",ratio=2)
                        Display.update_layout("BottomR",Enemy.print_combat_stats(),Enemy.name,ratio=6)
                        sleep(1/self.settings['CombatSpeed'])
                        if Enemy.Health == 0:
                            combat_text.append(f"{Enemy.name} has been defeated\n+{Enemy.ExpDrop}Exp")
                            Display.update_layout("MainTop",combat_text,"Press any key to continue",ratio=2)
                            Key.get_input()
                            # DROP LOOT AND SHIT
                            self.player.Exp += Enemy.ExpDrop
                            combat_text = Enemy.LootTable.Drop(self.player)
                            if combat_text == False:
                                break
                            Display.update_layout("MainTop",combat_text,"Press any key to continue",ratio=2)
                            Key.get_input()
                            break
                        # ENEMY TURN
                        combat_text.append(Enemy.Damage(self.player))
                        Display.update_layout("MainTop",combat_text,"Combat in progress",ratio=2)
                        Display.update_layout("BottomL",self.player.print_combat_stats(),self.player.name,ratio=6)
                        sleep(1/self.settings['CombatSpeed'])
                        if self.player.Health == 0:
                            combat_text.append(f"You have been defeated")
                            # FUCKING DIE LOL
                            Display.update_layout("MainTop",combat_text,"Press any key to continue",ratio=2)
                            Key.get_input()
                            Display.update_layout("MainTop",ratio=0)
                            return True
                        sleep(1/self.settings['CombatSpeed'])

        Display.update_layout("MainTop",ratio=0)
    
    def InventoryScreen(self):
            activeWindow = 0 # 0-inventory 1-equipment
            currentPage = 0
            itemsPerPage = 25
            targetInventory = 0
            targetEquipement = 0
            while True:
                info_screen = Text()
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
                            InventoryScreen.append(f">{Item.name}\n" ,style=f"u {Color.HIGHLIGHT_COLOR}")
                            targetItem = Item
                            info_screen.append(targetItem.print_stats())
                        else: InventoryScreen.append(f"{Item.name}\n" ,style=f"{Color.TEXT_COLOR}")
                if targetInventory == ExitIndex and activeWindow == 0: InventoryScreen.append(">Back\n" ,style=f"u {Color.GO_BACK_COLOR}")
                elif activeWindow == 0: InventoryScreen.append("Back\n" ,style=f"{Color.TEXT_COLOR}")

                for index, slot in enumerate(self.player.Equipment):
                    if index == targetEquipement and activeWindow == 1:
                        if self.player.Equipment[slot] != None:
                            EquipementScreen.append(f"{slot}: {self.player.Equipment[slot].name}\n" ,style=f"u {Color.HIGHLIGHT_COLOR}")
                            targetItem = self.player.Equipment[slot]
                            info_screen.append(targetItem.print_stats())
                        else: EquipementScreen.append(f"{slot}: {self.player.Equipment[slot]}\n" ,style=f"u {Color.HIGHLIGHT_COLOR}")
                        targetSlot = slot
                    else:
                        if self.player.Equipment[slot] != None: EquipementScreen.append(f"{slot}: {self.player.Equipment[slot].name}\n" ,style=f"{Color.TEXT_COLOR}")
                        else: EquipementScreen.append(f"{slot}: {self.player.Equipment[slot]}\n" ,style=f"{Color.TEXT_COLOR}")
                if targetEquipement == ExitIndex and activeWindow == 1: EquipementScreen.append(">Back\n" ,style=f"u {Color.GO_BACK_COLOR}")
                elif activeWindow == 1: EquipementScreen.append("Back\n" ,style=f"{Color.TEXT_COLOR}")

                if targetInventory == ExitIndex and activeWindow == 0: info_screen = self.player.print_stats()
                if targetEquipement == ExitIndex and activeWindow == 1: info_screen = self.player.print_stats()

                Display.update_layout("TopL",InventoryScreen,f"Inventory Page {currentPage+1}/{len(Pages)}",ratio=1)
                Display.update_layout("TopR",EquipementScreen,"Equipment",ratio=2)
                Display.update_layout("BottomL","",ratio=0)
                Display.update_layout("BottomR",info_screen,"Description" if targetItem != None else None,ratio=6)
                Display.update_layout("Left",ratio=1)
                Display.update_layout("Right",ratio=1)
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
                            Display.update_layout("BottomR",targetItem.Use(self.player),title="Press ANY key")
                            Key.get_input()
                        elif activeWindow == 1 and targetItem != None:
                            Display.update_layout("BottomR",self.player.UnequipItem(targetSlot),title="Press ANY key")
                            Key.get_input()
                    case Key.KEY_ESC:
                        return

    def generate_shop_items(self):
        self.shopInventory = []
        for x in range(50):
            newItem = copy(itemDB.__dict__[random.randint(0,len(itemDB.__dict__)-1)])
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
            info_screen = Text()
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
                        InventoryScreen.append(f">{Item.name}\n" ,style=f"u {Color.HIGHLIGHT_COLOR}")
                        targetItem = Item
                        info_screen.append(targetItem.print_stats())
                    else: InventoryScreen.append(f"{Item.name}\n" ,style=f"{Color.TEXT_COLOR}")
            if targetInventory == ExitIndex and activeWindow == 0: InventoryScreen.append(">Back\n" ,style=f"u {Color.GO_BACK_COLOR}")
            elif activeWindow == 0: InventoryScreen.append("Back\n" ,style=f"{Color.TEXT_COLOR}")

            if len(ShopPages[currentShopPage]) > 0:
                for index, Item in enumerate(ShopPages[currentShopPage]):
                    if index == targetShop and activeWindow == 1: 
                        ShopScreen.append(f">{Item.name}\n" ,style=f"u {Color.HIGHLIGHT_COLOR}")
                        targetItem = Item
                        info_screen.append(targetItem.print_stats())
                    else: ShopScreen.append(f"{Item.name}\n" ,style=f"{Color.TEXT_COLOR}")
            if targetShop == ExitIndex and activeWindow == 1: ShopScreen.append(">Back\n" ,style=f"u {Color.GO_BACK_COLOR}")
            elif activeWindow == 1: ShopScreen.append("Back\n" ,style=f"{Color.TEXT_COLOR}")

            if activeWindow == 0 and targetInventory == ExitIndex:
                info_screen.append(Ascii.back())
                info_screen.justify='center'
            if activeWindow == 1 and targetShop == ExitIndex:
                info_screen.append(Ascii.back())
                info_screen.justify='center'

            Display.update_layout("MainTop",info_screen,f"{self.player.Coins} Coins",ratio=3)
            Display.update_layout("TopL",ratio=0)
            Display.update_layout("TopR",ratio=0)
            Display.update_layout("BottomL",InventoryScreen,f"Inventory Page {currentInventoryPage+1}/{len(InventoryPages)}",ratio=6)
            Display.update_layout("BottomR",ShopScreen,f"Shop Page {currentShopPage+1}/{len(ShopPages)}",ratio=6)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
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
        Display.update_layout("MainTop",visible=False)

    def TawernScreen(self):
        menus = [self.rest]
        options = ["Rest (5 Coins)","Back"]
        target = 0
        while True:
            info_screen = Display.options_to_text(options,target)
            DescriptionScreen = self.player.print_stats()
            Display.update_layout("TopL",info_screen,f"{self.player.Coins} Coins",ratio=1)
            Display.update_layout("TopR",DescriptionScreen,self.player.name,ratio=1)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
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
        for name,value in self.player.stats.items():
            if name[0:3] != "Max": continue
            if self.player.stats[name[3:len(name)]] >= value: continue
            self.player.stats[name[3:len(name)]] = value
            text.append(f"{name[3:len(name)]} is restored\n")
        text.append("\nPress any key to continue")
        Display.update_layout("TopL","You are resting",ratio=1)
        sleep(0.4)
        Display.update_layout("TopL","You are resting.",ratio=1)
        sleep(0.4)
        Display.update_layout("TopL","You are resting..",ratio=1)
        sleep(0.4)
        Display.update_layout("TopL","You are resting...",ratio=1)
        sleep(0.4)
        Display.update_layout("TopL",text,ratio=1)
        Display.update_layout("TopR",self.player.print_stats(),self.player.name,ratio=1)
        self.Tick()
        Key.get_input()

    def LoadScreen(self):
        targetSaveOption = 0
        SaveOptions = ['Load','Menu','Delete']
        target = 0
        while True:
            saves = []
            for file in os.listdir(SAVE_FILE_PATH):
                filename = os.fsdecode(file)
                if filename.endswith(".json"): 
                    saves.append(filename.split(".json")[0])
            if saves == []: return self.NewGameScreen()
            SaveListText = Text(justify="right")
            SaveOptionText = Text()

            for index,saveName in enumerate(saves):
                if target == index:
                    SaveListText.append(f">{saveName}\n",style=f"{Color.HIGHLIGHT_COLOR}")
                    for optionIndex,option in enumerate(SaveOptions):
                        if targetSaveOption == len(SaveOptions)-1 and optionIndex == targetSaveOption:
                             SaveOptionText.append(f"{option}",style=f"u {Color.DANGER_COLOR}")
                        elif targetSaveOption == optionIndex:
                            SaveOptionText.append(f"{option}",style=f"u {Color.HIGHLIGHT_COLOR}")
                        else:
                            SaveOptionText.append(f"{option}",style=f"{Color.TEXT_COLOR}")
                        SaveOptionText.append(" ",style=None)
                    SaveOptionText.append("\n")
                    data = {}
                    with open(SAVE_FILE_PATH+"/"+saveName+".json", "r") as read_file:
                        data = json.load(read_file)
                        read_file.close()
                    SaveOptionText.append(f"{data['name']}\n")
                    SaveOptionText.append(f"Class: {data['stats']['Class']}\nLevel: {data['stats']['Level']}\nTurn-{data['tick']}\n")
                else:
                    SaveOptionText.append("\n")
                    SaveListText.append(f"{saveName}\n",style=f"{Color.TEXT_COLOR}")

            Display.update_layout("TopL",SaveListText,"Saves",ratio=1)
            Display.update_layout("TopR",SaveOptionText,"Actions",ratio=1)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=1)
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
            Display.update_layout("TopL","",ratio=1)
            Display.update_layout("TopR",fileText,ratio=1)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR",text,title="Press Y key to delete",ratio=3)
            Display.update_layout("Left",ratio=0)
            Display.update_layout("Right",ratio=1)
            match Key.get_input():
                case Key.KEY_y:
                    os.remove(f"{SAVE_FILE_PATH}/{SaveName}.json")
                    return
                case _:
                    return
 
    def ContinueSave(self):
        pass

    def SaveScreen(self):
        target = 0
        while True:
            saves = ['New Save File']
            for file in os.listdir(SAVE_FILE_PATH):
                filename = os.fsdecode(file)
                if filename.endswith(".json"): 
                    saves.append(filename.split(".json")[0])
            if saves == []: return self.NewGameScreen()
            SaveListText = Text()

            for index,saveName in enumerate(saves):
                if target == 0 and index == 0:
                    SaveListText.append(f">{saveName}\n",style=f"{Color.NEW_SAVE_FILE}")
                elif target == index:
                    SaveListText.append(f">{saveName}\n",style=f"{Color.HIGHLIGHT_COLOR}")
                else:
                    SaveListText.append(f"{saveName}\n",style=f"{Color.TEXT_COLOR}")

            Display.update_layout("TopL","",ratio=1)
            Display.update_layout("TopR",SaveListText,ratio=1)
            Display.update_layout("BottomL","",ratio=0)
            Display.update_layout("BottomR","",ratio=0)
            Display.update_layout("Left",ratio=1)
            Display.update_layout("Right",ratio=2)
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
            text.append(f"{userSaveName}" if userSaveName != "" else f"'{self.player.name}'")
            Display.update_layout("MainTop",text,"Save file name:",ratio=2)
            userInput = msvcrt.getwch()
            if userInput == '\r':
                if userSaveName == "":
                    userSaveName = self.player.name
                if os.path.exists(f"{SAVE_FILE_PATH}/{userSaveName}.json"):
                    overwriteText = Text("Save file already exists\n",justify='center')
                    overwriteText.append(f"{userSaveName}\n",style=f"{Color.DANGER_COLOR}")
                    overwriteText.append(f"Press Y to overwrite\n")
                    if self.confirm_screen(overwriteText):
                        self.SaveGame(userSaveName)
                        Display.update_layout("MainTop",visible=False)
                        return True
                    else:
                        break
                self.SaveGame(userSaveName)
                Display.update_layout("MainTop",visible=False)
                return True
            elif userInput == '\x1b':
                break
            elif userInput == '\x08':
                userSaveName = userSaveName[:-1]
            elif userInput == '\t' or userInput == '\x00':
                pass
            elif len(userSaveName) < 22:
                userSaveName += str(userInput)
        Display.update_layout("MainTop",visible=False)

          