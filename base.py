import pygame as pg
import numpy as np
from constants import *


class Level:
    def __init__(self, objects: dict):
        self.objects = objects

    def update(self, world):
        if world.time in self.objects:
            for obj in self.objects[world.time]:
                match obj[0]:
                    case 0: world.other = np.append(world.other, obj[1]())
                    case 1: world.enemies = np.append(world.enemies, obj[1]())


class Object:
    def __init__(self, rect: tuple or list, color: tuple or list, image: pg.Surface, time: int = 0, future_type: int = 0):
        self.image = image.convert()
        self.color = np.array(color)
        self.time = time
        self.future_type = future_type
        if len(rect) == 2:
            self.rect = np.array([*rect, *self.image.get_size()])
        else:
            self.rect = np.array(rect)
            pg.transform.scale(self.image, self.rect[2:])

    def update(self, world, time) -> list:
        return [self.future_type, self.rect, self.color, FUTURE]

    def get_time(self, time):
        return time - self.time

    def set_future(self, world):
        world.effects.append(self.update(world, world.time + FUTURE))


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
                np.append(collided, enemy)
            if world.teleport_allowed and \
                    self.rect[0] < enemy.rect[0] + enemy.rect[2] and \
                    self.rect[0] + self.rect[2] > enemy.rect[0] and \
                    self.rect[1] < enemy.rect[1] + enemy.rect[3] and \
                    self.rect[1] + self.rect[3] > enemy.rect[1]:
                np.append(collided, enemy)
        for enemy in collided:
            self.hp -= enemy.damage

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


class Enemy(Object):
    def __init__(self, rect: list or tuple, color: list or tuple, image: pg.Surface, damage: int, time: int = 0, future_type: int = 0):
        super().__init__(rect, color, image, time, future_type)
        self.damage = damage
