import pygame as pg
from settings import Settings
import game_functions as gf

from ship import Ship
from alien import Aliens
from game_stats import GameStats
from button import Play_Button, High_Score_Button
from scoreboard import Scoreboard
from sound import Sound
from barrier import Barriers
from main_menu import Main_Menu
import time



class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        ship_image = pg.image.load('images/ship.png')

        self.ship_height = ship_image.get_rect().height
        self.hs = 0
        self.sound = Sound(bg_music="sounds/spaceshooter.wav")
        self.sound.play()
        self.sound.pause_bg()
        self.play_button = self.aliens = self.stats = self.sb = self.bullets = self.ship = None
        self.hs_button = self.aliens = self.stats = self.sb = self.bullets = self.ship = None
        self.restart()

    def play(self):
        while True:
            gf.check_events(stats=self.stats, play_button=self.play_button, hs_button=self.hs_button, ship=self.ship, sound=self.sound)
            if self.stats.game_active:
                self.ship.update()
                self.barriers.update()
                self.aliens.update()

            self.screen.fill(self.settings.bg_color)
            self.ship.draw()
            self.aliens.draw()
            self.barriers.draw()
            self.sb.show_score()
            if not self.stats.game_active:
                menu = Main_Menu(screen=self.screen)
                menu.draw()
                self.play_button.draw()
                self.hs_button.draw()
                self.sound.pause_bg()
                if self.stats.show_high_score:
                    self.sb.show_score()
            else:
                if not self.sound.playing_bg: self.sound.unpause_bg()
            pg.display.flip()

    def restart(self):
        self.play_button = Play_Button(screen=self.screen, msg="Play")
        self.hs_button = High_Score_Button(screen=self.screen, msg="High Score")
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(game=self, sound=self.sound)
        self.settings.init_dynamic_settings()

        self.barriers = Barriers(game=self)
        self.aliens = Aliens(ship_height=self.ship_height, game=self, barriers=self.barriers)
        self.ship = Ship(aliens=self.aliens, sound=self.sound, game=self, barriers=self.barriers)
        self.aliens.add_ship(ship=self.ship)
        self.stats.high_score = self.hs
        self.sb.prep_high_score()

    def reset(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ship.center_ship()
            time.sleep(0.5)
            self.ship.timer = Ship.timer
        else:
            self.stats.game_active = False
            self.stats.show_high_score = False
            self.sound.pause_bg()
            self.hs = self.stats.high_score
            self.restart()

def main():
    g = Game()
    g.play()



if __name__ == '__main__':
    main()

