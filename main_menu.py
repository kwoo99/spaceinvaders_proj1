import pygame as pg
import pygame.font
from pygame.sprite import Sprite

class Main_Menu(Sprite):

    menu_image = pg.image.load('images/main_menu.png')
    menu_rect = (0, 0)

    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.screen_rect.center = (0, 0)
        self.width, self.height = 1200, 800


    def draw(self):
        self.screen.blit(self.menu_image, self.menu_rect)