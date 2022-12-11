import numpy as np
import pygame as pg
from constants import *
from base import Object


class Player(Object):
    def __init__(self, rect: tuple or list, color: list or tuple, image: pg.Surface, hp: int = DEFHP):
        super().__init__(rect, color, image)
        self.hp = hp
        self.second_rect = np.array([0, 0])

    def update(self, world):
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
                    self.second_rect[0] + self.second_rect[2] > enemy.rect[0] and \
                    self.second_rect[1] < enemy.rect[1] + enemy.rect[3] and \
                    self.second_rect[3] + self.second_rect[1] > enemy.rect[1]:
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