import pygame as pg
import numpy as np
from constants import *
from base import Level
from player import Player
import os


class World:
    def __init__(self):
        self.player = Player(PSIZE, (240, 200, 200), pg.Surface((50, 50)))
        self.player.image.fill((240, 200, 200))
        self.level = Level({})
        self.enemies = np.array([])
        self.other = np.array([])
        self.effects = [np.array([[-1, None, None, None]], ndmin=2), np.array([[-1, None, None, None]], ndmin=2)]
        # self.effects = np.array([[-1, None, None, None]], ndmin=2)
        self.time = 0
        self.updates = True
        self.teleport_allowed = False

    def update(self):
        self.level.update(self)
        deleted = 0
        for i, enemy in enumerate(self.enemies):
            upd = enemy.update(self)
            if upd[0] == -1:
                self.enemies = np.delete(self.enemies, i-deleted)
                deleted += 1
                continue
            enemy.rect = upd[1]
            enemy.set_future(self)
        deleted = 0
        for i, other in enumerate(self.other):
            upd = other.update(self)
            if upd[0] == -1:
                self.other = np.delete(self.other, i-deleted)
                deleted += 1
                continue
            other.rect = upd[1]
            # other.set_future(self)
        self.player.update(self)
        if self.updates: self.time += 1

    def game_over(self):
        self.updates = False
        self.time = 0
        self.enemies = np.array([])
        self.player.game_over = 1

    def load_level(self, name):
        if os.path.isfile(f'levels/{name}.py'):
            level = __import__(f'levels.{name}', None, None, name)
            self.enemies = level.enemies
            self.other = level.other
            self.level = level.level
        else:
            print(f'{name} level is not found')


class Paint:
    def __init__(self):
        self.screen = pg.display.set_mode(SSIZE)

    def fill_background(self, color: tuple = DEF_BG_COLOR):
        self.screen.fill(color)

    def draw_player(self, world):
        # self.screen.blit(world.player.image, world.player.rect[:2])
        pg.draw.rect(self.screen, world.player.color, world.player.rect, max(1, int(world.player.hp * HPCOEFF // 4)))
        if world.player.second_rect[0]:
            self.screen.blit(world.player.image, world.player.second_rect)

    def draw_enemies(self, world: World):
        for enemy in world.enemies:
            self.screen.blit(enemy.image, enemy.rect[:2])

    def draw_other(self, world: World):
        for obj in world.other:
            self.screen.blit(obj.image, obj.rect[:2])

    def draw_effects(self, world: World, upper: bool = False):
        deleted = 0
        for i, r in enumerate(world.effects[upper]):
            if r[0] == -1:
                world.effects[upper] = np.delete(world.effects[upper], i-deleted, axis=0)
                deleted += 1
            elif r[0] == 0:
                pg.draw.rect(self.screen, r[2] // 4, r[1])
                world.effects[upper][i-deleted, 3] -= 1
                if r[3] <= 0:
                    world.effects[upper] = np.delete(world.effects[upper], i-deleted, axis=0)
                    deleted += 1
            elif r[0] == 1:
                color = (np.array(DEF_BG_COLOR) * r[3] + r[2] * (FUTURE - r[3])) // FUTURE
                pg.draw.rect(self.screen, color, r[1])
                world.effects[upper][i-deleted, 3] -= 1
                if r[3] <= 0:
                    world.effects[upper] = np.delete(world.effects[upper], i-deleted, axis=0)
                    deleted += 1
        # world.effects[:, 3] -= 1

    def draw_everything(self, world):
        self.draw_effects(world)
        self.draw_other(world)
        self.draw_enemies(world)
        self.draw_effects(world, True)
        self.draw_player(world)


class Main:
    def __init__(self):
        self.paint = Paint()
        self.world = World()
        self.clock = pg.time.Clock()

    def update(self):
        self.paint.fill_background()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        self.world.update()
        self.paint.draw_everything(self.world)
        pg.display.update()
        self.clock.tick(60)
        return True

    def run(self):
        while self.update(): pass


if __name__ == '__main__':
    main = Main()
    main.world.load_level('test_level')
    main.run()
