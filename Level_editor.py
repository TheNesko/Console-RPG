import pygame, pickle
import CursedEngine as ce
from math import floor
from pygame.locals import *


class Grid():

    def __init__(self) -> None:
        super().__init__()
        self.cell_size = 32
        self.grid = []
        self.levels = []
    
    def generate_grid(self,map_size,block_size=None):
        if block_size != None: self.cell_size = block_size
        for width in range(map_size[0]):
            self.grid.append([])
            for height in range(map_size[1]):
                self.grid[width].append([])
                self.grid[width][height] = 0
    
    def get_grid_position(self,position):
        gridPos = ( floor(position[0]/self.cell_size) , floor(position[1]/self.cell_size) )
        if gridPos[0] > len(self.grid) or gridPos[0] < 0: return
        if gridPos[1] > len(self.grid[0]) or gridPos[1] < 0: return
        return gridPos

    def draw_grid_lines(self,screen,offset):
        for x in range(len(self.grid)):
            pygame.draw.line(screen,(30,30,30),(x*self.cell_size+offset[0],0+offset[1]),(x*self.cell_size+offset[0],1000*self.cell_size+offset[1]))
        for y in range(len(self.grid[0])):
            pygame.draw.line(screen,(30,30,30),(0+offset[0],y*self.cell_size+offset[1]),(1000*self.cell_size+offset[0],y*self.cell_size+offset[1]))

    def save_to_file(self):
        with open("GameMap.map", "wb") as write_file:
            pickle.dump(self.grid,write_file)
            write_file.close()

    def load_from_file(self):
        LoadedMap = []
        with open("GameMap.map", "rb") as write_file:
            LoadedMap = pickle.load(write_file)
            write_file.close()
        for width in range(len(LoadedMap)-1):
            for height in range(len(LoadedMap[width])-1):
                self.grid[width][height] = LoadedMap[width][height]


def main():
    width = 800
    height = 600

    x_offset = 0
    y_offset = 0

    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Level Editor')

    grid = Grid()
    grid.generate_grid((100,50),32)
    grid.load_from_file()

    save_button = ce.Button((0,height-30),(width/2-10,30),(255,150,0),f"Save",(0,0,0),40)
    load_button = ce.Button((width/2+10,height-30),(width/2,30),(255,150,0),f"Load",(0,0,0),40)

    block_id = 0
    colors = [(10,100,10),(10,40,10),(100,10,60),(10,10,100),(20,50,40)]
    '''
    Tile id:
    0 - Forest
    1 - DenceForest
    2 - Road
    3 - Town
    4 - Village
    '''

    Clock = pygame.time.Clock()
    is_running = True
    while is_running:
        ce.events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    ce.events.append(ce.MOUSE_LEFT)
            if event.type == pygame.MOUSEWHEEL:
                grid.cell_size += event.y
                if grid.cell_size > 32: grid.cell_size = 32
                if grid.cell_size < 8: grid.cell_size = 8
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    save_button.visible = not save_button.visible
                    load_button.visible = not load_button.visible


        screen.fill((30,30,30))
        delta = Clock.tick(60)/1000

        ce.UI.Update()

        if save_button.is_pressed: grid.save_to_file()
        if load_button.is_pressed: grid.load_from_file()
        camera_speed = 10
        if pygame.key.get_pressed()[pygame.K_a]:
            x_offset += camera_speed*grid.cell_size*delta
        if pygame.key.get_pressed()[pygame.K_d]:
            x_offset -= camera_speed*grid.cell_size*delta
        if pygame.key.get_pressed()[pygame.K_s]:
            y_offset -= camera_speed*grid.cell_size*delta
        if pygame.key.get_pressed()[pygame.K_w]:
            y_offset += camera_speed*grid.cell_size*delta
        
        if pygame.key.get_pressed()[pygame.K_1]:
            block_id = 0
        if pygame.key.get_pressed()[pygame.K_2]:
            block_id = 1
        if pygame.key.get_pressed()[pygame.K_3]:
            block_id = 2
        if pygame.key.get_pressed()[pygame.K_4]:
            block_id = 3
        if pygame.key.get_pressed()[pygame.K_5]:
            block_id = 4
        # if pygame.key.get_pressed()[pygame.K_6]:
        #     block_id = 5
        # if pygame.key.get_pressed()[pygame.K_7]:
        #     block_id = 6
        

        mouse_pressed = pygame.mouse.get_pressed()
        local_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (local_mouse_pos[0]-x_offset,local_mouse_pos[1]-y_offset)
        if mouse_pressed[0]:
            if ce.UI.is_over_ui == False:
                grid_pos = grid.get_grid_position(mouse_pos)
                if grid_pos != None: 
                    grid.grid[grid_pos[0]][grid_pos[1]] = block_id
        if mouse_pressed[2]:
            if ce.UI.is_over_ui == False:
                grid_pos = grid.get_grid_position(mouse_pos)
                if grid_pos != None: 
                    grid.grid[grid_pos[0]][grid_pos[1]] = 0


        for width in range(len(grid.grid)-1):
            for height in range(len(grid.grid[width])-1):
                cellID = grid.grid[width][height]
                cell = pygame.Rect(width*grid.cell_size+x_offset,height*grid.cell_size+y_offset,grid.cell_size,grid.cell_size)
                pygame.draw.rect(screen,colors[cellID],cell)

        grid.draw_grid_lines(screen,(x_offset,y_offset))
        ce.UI.Draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main()