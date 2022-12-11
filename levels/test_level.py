from base import Enemy, Level
import pygame as pg
import math as m
import numpy as np
from constants import *


class Righter(Enemy):
    def __init__(self, pos: tuple, time=0):
        image = pg.Surface((80, 80))
        image.fill((210, 165, 140))
        self.pos = pos
        # super().__init__(pos, (210, 165, 140), image, 5, time, 0)
        super().__init__(pos, (210, 165, 140), image, 1, time, 0)

    def update(self, world, time=None) -> list:
        if time is None: time = world.time
        time = self.get_time(time)
        rect = self.rect.copy()
        rect[0] = time * 5 + self.pos[0]
        if self.rect[0] > SWIDTH:
            return [-1, None, None, None]
        return [self.future_type, rect, self.color, FUTURE]


class ModyRighter(Righter):
    def update(self, world, time=None):
        if time is None: time = world.time
        ft, rect, c, _ = super().update(world, time)
        # time = self.get_time(time)
        if ft == -1: return [-1, None, None, None]
        rect[1] = self.pos[1] + m.sin(m.radians(time)) * 75
        return [ft, rect, c, FUTURE]


level = {
    10: [[1, lambda: Righter((-500-FUTURE, 30), 10)]],
    30: [[1, lambda: Righter((-500-FUTURE, 400), 30)]],
    350: [[1, lambda: ModyRighter((-500-FUTURE, SHEIGHT//2), 350)]],
    400: [[1, lambda: ModyRighter((-500-FUTURE, SHEIGHT//4), 400)]],
    450: [[1, lambda: ModyRighter((-500-FUTURE, SHEIGHT//3*2), 450)]],
    500: [[1, lambda: ModyRighter((-500-FUTURE, SHEIGHT//2), 500)]],
    550: [[1, lambda: ModyRighter((-500-FUTURE, SHEIGHT//6), 550)]],
    600: [[1, lambda: ModyRighter((-500-FUTURE, SHEIGHT//12*7), 600)]],
}
level = Level(level)

enemies = np.array([Righter((-500-FUTURE, 300))])
other = np.array([])
__all__ = [level, enemies, other]
