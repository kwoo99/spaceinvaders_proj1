import sys
import pygame as pg

def check_keydown_events(event, ship, sound):
    if event.key == pg.K_RIGHT: ship.moving_right = True
    elif event.key == pg.K_LEFT: ship.moving_left = True
    elif event.key == pg.K_SPACE: ship.shooting_bullets = True
    elif event.key == pg.K_q: sys.exit()

def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT: ship.moving_right = False
    elif event.key == pg.K_LEFT: ship.moving_left = False
    elif event.key == pg.K_SPACE: ship.shooting_bullets = False

def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

def check_high_score_button(stats, hs_button, mouse_x, mouse_y):
    if hs_button.rect.collidepoint(mouse_x, mouse_y):
        stats.show_high_score = True

def check_events(stats, play_button, hs_button, ship, sound):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            print("Debug")
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_high_score_button(stats=stats, hs_button=hs_button, mouse_x=mouse_x, mouse_y=mouse_y)
            check_play_button(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, ship=ship, sound=sound)
            print("Debug_Key_Down")
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event, ship=ship)
            print("Debug_Key_Up")
