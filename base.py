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
    def __init__(self, rect: tuple or list, image: pg.Surface, color: tuple or list, time: int = 0, future_type: int = 0):
        self.image = image.convert()
        self.color = np.array(color)
        self.time = time
        self.future_type = future_type
        if len(rect) == 2:
            self.rect = np.array([*rect, *self.image.get_size()])
        else:
            self.rect = np.array(rect)
            self.image = pg.transform.scale(self.image, self.rect[2:])

    def update(self, world, time: int = None) -> list:
        return [self.future_type, self.rect, self.color, FUTURE]

    def get_time(self, time: int) -> int:
        return time - self.time

    def set_future(self, world):
        world.effects[0] = np.append(world.effects[0], np.array(self.update(world, world.time + FUTURE), ndmin=2, dtype=object), axis=0)
        pass


class Enemy(Object):
    def __init__(self, rect: list or tuple, image: pg.Surface, color: list or tuple, damage: int, time: int = 0, future_type: int = 0):
        super().__init__(rect, image, color, time, future_type)
        self.damage = damage
