import pygame as pg
from pygame.sprite import Sprite
from pygame.sprite import Group
from copy import copy
from timer import Timer

class Barriers(Sprite):
    def __init__(self, game):
        self.barriers = [Barrier(game=game, x=x, y=650) for x in range(250, 1050, 200)]

        self.barriers_group = Group()
        for barrier in self.barriers:
            self.barriers_group.add(barrier.barrier_group.sprites())

    def group(self): return self.barriers_group

    def update(self):
        super().__init__()
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()

class Barrier(Sprite):
    images = [pg.image.load('images/ship.png')]
    block = pg.image.load('images/block.png')
    topcornerL = pg.image.load('images/topcornerL.png')
    topcornerR = pg.image.load('images/topcornerR.png')
    block_rect = block.get_rect()
    height, width = block_rect.width, block_rect.height
    barrier_height = 5
    barrier_width = 7

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.x, self.y = x, y
        self.rect = copy(Barrier.block_rect)
        self.screen_rect = game.screen.get_rect()
        self.rect.x, self.rect.y = x, y
        self.barrier_group = Group()
        self.create_barrier()

    def create_barrier(self):
        w, h = Barrier.block_rect.width, Barrier.block_rect.height
        rect = copy(self.rect)
        for x in range(Barrier.barrier_width):
            for y in range(Barrier.barrier_height):
                if y >= Barrier.barrier_height - 1 and 2 <= x <= 4: continue
                r = copy(rect)
                image = self.block
                if y == 0 and x == 0: image = self.topcornerL
                elif y == 0 and x == Barrier.barrier_width - 1: image = self.topcornerR
                r = copy(rect)
                r.y += h * y
                r.x += w * x
                self.barrier_group.add(BarrierBlock(parent=self, game=self.game, image=image, rect=r))

    def group(self): return self.barrier_group

    def update(self):
        self.barrier_group.update()
        for block in self.barrier_group:
            block.update()

    def draw(self):
        for block in self.barrier_group:
            block.draw()

class BarrierBlock(Sprite):
    Normal = 4
    Scathed = 3
    Heavily_Damaged = 2
    Critical = 1
    Terminated = 0

    def __init__(self, parent, game, image, rect):
        super().__init__()
        self.parent = parent
        self.game = game
        self.image = image
        self.screen = game.screen
        self.rect = rect
        self.health = BarrierBlock.Normal

    def damaged(self):
        health = self.health
        if health is not BarrierBlock.Terminated:
            self.health -= 1

    def update(self): pass

    def draw(self):
        self.screen.blit(self.image, self.rect)
