import pygame
from pygame.locals import *

MOUSE_LEFT = "m_l"
MOUSE_RIGHT = "m_r"

events = []

class UI():
    Objects = []

    is_over_ui = False

    def __init__(self) -> None:
        UI.Objects.append(self)

    def Draw(Screen) -> None:
        for Object in UI.Objects:
            Object.Draw(Screen)

    def Update() -> None:
        UI.is_over_ui = False

        for Object in UI.Objects:
            Object.Update()

class Button(UI):
    def __init__(self,position,size,color=(255,255,255),text="",text_color=(255,255,255),font_size=20,visible=True) -> None:
        super().__init__()
        self.rect = pygame.Rect(position[0],position[1],size[0],size[1])
        self.text = text
        self.text_color = text_color
        self.color = color
        self.is_pressed = False
        self.visible = visible
        self.font1 = pygame.font.SysFont("didot.ttc", font_size)
        self.img = self.font1.render(self.text, True, self.text_color)
    
    def Draw(self,Screen) -> None:
        if self.visible:
            pygame.draw.rect(Screen,self.color,self.rect)
            self.img = self.font1.render(self.text, True, self.text_color)
            img_rect = self.img.get_rect(center=self.rect.center)
            Screen.blit(self.img,img_rect)

    def Update(self) -> None:
        self.is_pressed = False
        if self.visible:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos[0],mouse_pos[1]):
                UI.is_over_ui = True
                if MOUSE_LEFT in events:
                    self.is_pressed = True

class Popup(UI):
    def __init__(self) -> None:
        super().__init__()