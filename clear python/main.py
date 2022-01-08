from environment import Environment
from button import Button
import pygame as pg
import random as rand
import math
import sys


def left_click():
    global l_press
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1 and not l_press:
            l_press = True
            return True
    elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 1:
            l_press = False
    return False


def right_click():
    global r_press
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 3 and not r_press:
            r_press = True
            return True
    elif event.type == pg.MOUSEBUTTONUP:
        if event.button == 3:
            r_press = False
    return False


# global references
try:
    WIDTH, HEIGHT = int(sys.argv[1]), int(sys.argv[2])
except IndexError:
    WIDTH, HEIGHT = 1280, 720
TICK_RATE = 5

l_press = False
r_press = False

if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode((WIDTH, HEIGHT), vsync=1)
    clock = pg.time.Clock()

    pg.font.init()
    font = pg.font.Font("font.ttf", 24)
    font_im = pg.font.Font("font.ttf", 48)

    # creating the game logic / environment sample

    env = Environment()

    btns = [Button((200, 120), (300, 140), "dynamic", env.update),
            Button((200, 150), (300, 170), "dynamic", env.update),
            Button((200, 180), (300, 200), "dynamic", env.update)]

    upd_ticks = pg.time.get_ticks()

    btn_sprite = pg.image.load("sprites/plate.png")
    cave_texture = pg.image.load("sprites/cave.png")
    wumpus_sprite = pg.image.load("sprites/wumpus.png")
    btn_sprite = pg.transform.scale(btn_sprite, (195, 180))
    cave_texture = pg.transform.scale(cave_texture, (WIDTH / 4, HEIGHT / 4))
    cave_texture = pg.transform.scale(cave_texture, (WIDTH, HEIGHT))
    wumpus_sprite = pg.transform.scale(wumpus_sprite, (300, 300))

    # main cycle
    while True:
        # surfaces cleaning
        # screen.fill((140, 140, 140))
        screen.blit(cave_texture, (0, 0))
        
        # checking for keyboard, window, mouse inputs or events
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_u:
                    TICK_RATE -= 1
                    upd_ticks = pg.time.get_ticks()
                if event.key == pg.K_i:
                    TICK_RATE += 1
                    upd_ticks = pg.time.get_ticks()

        if left_click():
            btns[0].coll(pg.mouse.get_pos(), 0)
            btns[1].coll(pg.mouse.get_pos(), 1)
            btns[2].coll(pg.mouse.get_pos(), 2)

        # game Assets/UI/elements drawing

        screen.blit(btn_sprite, (150, 70))

        for i, btn in enumerate(btns):
            # pg.draw.rect(screen, "green", btn.rect)
            room = font.render("go to " + str(env.agent.location.connects_to[i]) + "?", True, (0, 0, 0))
            screen.blit(room, btn.point1)

        text = font_im.render("I'm in " + str(env.agent.location.number) + " room.", True, (255, 255, 255))
        screen.blit(text, (400, 150))

        if env.state[8]:
            screen.blit(wumpus_sprite, (400, 200))

        pg.display.set_caption("$~Wumpus ~fps: " + str(round(clock.get_fps(), 2)) + " ~tickrate: " + str(TICK_RATE))

        pg.display.flip()
        clock.tick()
