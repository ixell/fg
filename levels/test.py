from base import Enemy, Level
import pygame as pg
import math as m
import numpy as np
from constants import FUTURE, SWIDTH


class Test(Enemy):
    def __init__(self, pos):
        image = pg.Surface((80, 80))
        image.fill((190, 210, 190))
        self.pos = pos
        super().__init__(pos, image, (190, 210, 190), 5)
        # super().__init__(pos, (190, 210, 190), image, 5, 0, 1)

    def update(self, world, time=None) -> list:
        if time is None: time = world.time
        rect = self.rect.copy()
        rect[0] = (time + self.pos[0]) % SWIDTH
        return [self.future_type, rect, self.color, FUTURE]


level = Level({})
enemies = np.array([Test((300, 300))])
other = np.array([])
__all__ = [enemies, other]
