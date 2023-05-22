from imports import *
try:
    from display import Display
    from input import Key
    from items import ItemClass
except:
    pass

GAME_VERSION = "0.1"
SAVE_FILE_PATH = os.getenv('APPDATA')+"\RPG_PYTHON"
if not os.path.exists(SAVE_FILE_PATH):
    os.mkdir(SAVE_FILE_PATH)


class Save:
    def LoadGame(self,SaveName:str):
        # CurrentSaveFileName = SaveName.split(".json")[0]
        data = {}
        with open(SAVE_FILE_PATH+"/"+SaveName+".json", "r") as read_file:
            data = json.load(read_file)
            read_file.close()

        if data['GameVersion'] != GAME_VERSION:
            while True:
                SaveVersionText = Text(f"Save version\n{data['GameVersion']}",justify="right")
                game_version_text = Text(f"Game version\n{GAME_VERSION}")
                text = Text("\n\nSave version is different from Game version\n",justify='center')
                text.append("Press Y key to continue\n")
                Display.update_layout("TopL",SaveVersionText,ratio=1)
                Display.update_layout("TopR",game_version_text,ratio=1)
                Display.update_layout("MainTop",text)
                if Key.get_input() != Key.KEY_y:
                    Display.update_layout("MainTop",visible=False)
                    return False
                else: break

        Display.update_layout("MainTop",visible=False)

        self.player.name = data['name']
        for SaveStat in data['stats']:
            if SaveStat in self.player.stats:
                self.player.stats[SaveStat] = data['stats'][SaveStat]
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
        self.player.tick_game_update = data['tick_game_update']
        try:
            pass
        except:
            pass
        
        return True
    
    def SaveGame(self,SaveName:str):
        Save = {
            'name' : self.player.name,
            'stats' : {},
            'Bonuses': {},
            'Inventory' : {},
            'Equipment' : {},
            'Location' : {},
            'GameVersion': GAME_VERSION,
            'tick': self.player.tick,
            'tick_game_update': self.player.tick_game_update,
        }
        for stat in self.player.stats:
            Save['stats'][stat] = self.player.stats[stat]
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
        
        with open(SAVE_FILE_PATH+"/"+SaveName +".json", "w") as write_file:
            json.dump(Save, write_file)
            write_file.close()
        # CurrentSaveFileName = SaveName