from imports import *
from characters import EnemyDataBase as enemyDB


class MapTile:
    tile_list = []

    def __init__(self,
                 name: str="Town",
                 map_symbol: str="#",
                 symbol_color: str="white",
                 hostile: bool=False,
                 enemies=[],
                 **content):
        MapTile.tile_list.append(self)
        self.name = name
        self.map_symbol = map_symbol
        self.symbol_color = symbol_color
        self.hostile = hostile
        self.enemies = enemies
        self.content = content
    
    def display_tile_info(self):
        text = Text()
        text.append(f"{self.name}\n")
        if self.hostile: text.append("Hostile\n",style="red")
        if self.content != {}: text.append("Activities:\n")
        for name, _ in self.content.items():
            text.append(f"*{name}\n")
        return text


class TileDataBase:
    forest = MapTile("Forest","T","green",False,[enemyDB.dummy])
    dence_forest = MapTile("Dence Forest","D","dark_green",True,[enemyDB.dummy,enemyDB.bandit])
    road = MapTile("Road","#","grey53",False,[enemyDB.bandit])
    town = MapTile("Town","█","royal_blue1",False)
    village = MapTile("Village","█","orange4",False)


class Map:
    game_map = []
    def __init__(self,
                 display_width: int=51,
                 display_height: int=21):
        game_map_file = []
        with open("GameMap.map", "rb") as write_file:
            game_map_file = pickle.load(write_file)
            write_file.close()
        self.generate_map(game_map_file)
        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        self.display_width = display_width
        self.display_height = display_height
        if self.display_width == None:
            self.display_width = self.width
        if self.display_height == None:
            self.display_height = self.height

    def generate_map(self, map_file):
        tile_base = MapTile.tile_list
        for height in range(len(map_file[0])):
            self.game_map.append([])
            for width in range(len(map_file)):
                self.game_map[height].append(tile_base[map_file[width][height]])

    def display_map(self, player_position):
        text = Text()
        x_range = range(self.display_width)
        y_range = range(self.display_height)
        # X MAP DISPLAY LIMIT 
        if player_position[0]-floor(self.display_width/2) > 0:
            x_range = range(player_position[0]-floor(self.display_width/2),
                            player_position[0]+ceil(self.display_width/2))
        if player_position[0]+ceil(self.display_width/2) > self.width:
            x_range = range(self.width-self.display_width, self.width)
        # Y MAP DISPLAY LIMIT 
        if player_position[1]-floor(self.display_height/2) > 0:
            y_range = range(player_position[1]-floor(self.display_height/2),
                            player_position[1]+ceil(self.display_height/2))
        if player_position[1]+ceil(self.display_height/2) > self.height:
            y_range = range(self.height-self.display_height, self.height)
        
        for y in y_range:
            for x in x_range:
                tile = self.game_map[y][x]
                if player_position[0] == x and player_position[1] == y:
                    text.append("@")
                    continue
                text.append(tile.map_symbol, tile.symbol_color)
            text.append("\n")
        return text

    def get_tile(self, position):
        return self.game_map[position[1]][position[0]]

