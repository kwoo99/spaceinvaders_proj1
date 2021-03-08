import pygame as pg
from pygame.sprite import Sprite
from pygame.sprite import Group
from bullet import Ship_Bullet
from timer import Timer

class Ship(Sprite):
    images = [pg.image.load('images/ship.png')]
    images_boom = [pg.image.load('images/ship_boom' + str(i) + '.png') for i in range(9)]
    timer = Timer(frames=images, wait=1000)
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, sound, game, barriers=None, aliens=None):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.sound = sound
        self.game = game
        self.barriers = barriers
        self.aliens = aliens

        self.image = pg.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()

        self.center = 0
        self.center_ship()

        self.moving_right = False
        self.moving_left = False

        self.shooting_bullets = False
        self.bullets_attempted = 0
        self.dead, self.reallydead, self.timer_switched = False, False, False
        self.ship_group = Group()
        self.ship_group.add(self)
        self.alien_killing_bullet = Group()
        self.timer = Ship.timer

    def add_bullet(self):
        self.alien_killing_bullet.add(Ship_Bullet(game=self.game, x=self.rect.centerx,y=self.rect.top))

    def group(self): return self.ship_group

    def killed(self):
        if not self.dead and not self.reallydead:
            self.dead = True
        if self.dead and not self.timer_switched:
            self.timer = Ship.timer_boom
            self.timer_switched = True

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def update(self):
        self.alien_killing_bullet.update()
        if self.dead and self.timer_switched:
            if self.timer.frame_index() == len(Ship.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.timer.reset()
                self.game.reset()
        bullet_alien_collisions = pg.sprite.groupcollide(self.aliens.group(), self.alien_killing_bullet, False, True)

        if bullet_alien_collisions:
            for alien in  bullet_alien_collisions:
                alien.dead = True
                alien.killed()

        bullet_barrier_collisions = pg.sprite.groupcollide(self.barriers.group(), self.alien_killing_bullet, True, True)

        if bullet_barrier_collisions:
            for barrier_block in bullet_barrier_collisions:
                barrier_block.damaged()

        if len(self.aliens.group()) == 0:
            self.alien_killing_bullet.empty()
            self.settings.increase_speed()
            self.aliens.create_fleet()
            self.game.stats.level += 1
            self.game.sb.prep_level()

        delta = self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right: self.center += delta
        if self.moving_left and self.rect.left > 0: self.center -= delta
        if self.shooting_bullets and not self.dead:
            self.sound.shoot_bullet()
            self.add_bullet()
            self.shooting_bullets = False
        self.rect.centerx = self.center

    def draw(self):
        for bullet in self.alien_killing_bullet:
            bullet.draw()
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
