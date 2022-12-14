import numpy as np
import pygame as pg
from constants import *
from base import Object


class Player(Object):
    def __init__(self, rect: tuple or list, color: list or tuple, image: pg.Surface, hp: int = DEFPHP):
        super().__init__(rect, color, image)
        self.game_over = 0
        self.color = list(color)
        self.hp = hp
        self.second_rect = np.array([0, 0])
        self.wait = 0

    def update(self, world):
        if self.wait:
            self.wait -= 1
        else:
            if self.game_over:
                if self.game_over == 1:
                    if self.color[0] < 255: self.color[0] = min(self.color[0] + 15, 255)
                    if self.color[1] < 255: self.color[1] = min(self.color[1] + 15, 255)
                    if self.color[2] < 255: self.color[2] = min(self.color[2] + 15, 255)
                    if self.hp < DEFPHP: self.hp = self.hp + 10
                    if self.color[0] == 255 and self.color[1] == 255 and self.color[2] == 255 and self.hp == DEFPHP:
                        self.wait = 2
                        self.game_over = 2
                else:
                    if self.color[0] > DEF_BG_COLOR[0]:
                        self.color[0] = max(self.color[0] - 10, DEF_BG_COLOR[0])
                        self.color[1] = max(self.color[1] - 10, DEF_BG_COLOR[1])
                        self.color[2] = max(self.color[2] - 10, DEF_BG_COLOR[2])
                self.image.fill(self.color)
            else:
                self.move()
                self.collide(world)
                self.wall_collide(world)

    def move(self):
        keys = pg.key.get_pressed()
        rect = np.array([0, 0])
        if keys[pg.K_a]: rect[0] -= PSPEED
        if keys[pg.K_d]: rect[0] += PSPEED
        if keys[pg.K_w]: rect[1] -= PSPEED
        if keys[pg.K_s]: rect[1] += PSPEED
        if rect[0] and rect[1]:
            self.rect[:2] += rect // 3 * 2
        else:
            self.rect[:2] += rect

    def collide(self, world):
        collided = np.array([])
        for enemy in world.enemies:
            if self.rect[0] < enemy.rect[0] + enemy.rect[2] and \
                    self.rect[0] + self.rect[2] > enemy.rect[0] and \
                    self.rect[1] < enemy.rect[1] + enemy.rect[3] and \
                    self.rect[1] + self.rect[3] > enemy.rect[1]:
                collided = np.append(collided, enemy)
            if world.teleport_allowed and \
                    self.second_rect[0] < enemy.rect[0] + enemy.rect[2] and \
                    self.second_rect[0] + self.rect[2] > enemy.rect[0] and \
                    self.second_rect[1] < enemy.rect[1] + enemy.rect[3] and \
                    self.rect[3] + self.second_rect[1] > enemy.rect[1]:
                collided = np.append(collided, enemy)
        for enemy in collided:
            self.hp -= enemy.damage
            if self.hp <= 0: world.game_over()
            print(self.hp)

    def wall_collide(self, world):
        if world.teleport_allowed:
            self.second_rect = self.rect.copy()
            if self.rect[0] + self.rect[2] > SWIDTH:
                if self.rect[0] > SWIDTH:
                    self.rect[0] = 0
                self.second_rect[0] = self.rect[0] - SWIDTH
            elif self.rect[0] < 0:
                if self.rect[0] < - self.rect[2]:
                    self.rect[0] = SWIDTH - self.rect[2]
                self.second_rect[0] = SWIDTH + self.rect[0]
            if self.rect[1] + self.rect[3] > SHEIGHT:
                if self.rect[1] > SHEIGHT:
                    self.rect[1] = 0
                self.second_rect[1] = self.rect[1] - SHEIGHT
            elif self.rect[1] < 0:
                if self.rect[1] < - self.rect[3]:
                    self.rect[1] = SHEIGHT - self.rect[3]
                self.second_rect[1] = SHEIGHT + self.rect[1]
        else:
            if self.rect[0] + self.rect[2] > SWIDTH:
                self.rect[0] = SWIDTH - self.rect[2]
            elif self.rect[0] < 0:
                self.rect[0] = 0
            if self.rect[1] + self.rect[3] > SHEIGHT:
                self.rect[1] = SHEIGHT - self.rect[3]
            elif self.rect[1] < 0:
                self.rect[1] = 0
