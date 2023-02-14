import pygame as pg

q = False
mini_map = [
    [5, 5, 5, 5, 2, 2, 5, 2, 5, 5, 2, 5, 2, 2, 5, 5],
    [5, 2, q, q, q, q, q, q, 6, q, q, q, q, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 5, q, q, 2, 6, 5, q, q, q, 2, 6, q, q, 2, 5],
    [5, 5, q, q, q, q, q, q, q, q, q, q, q, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 5, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 5, 5],
    [5, 5, q, 1, 5, 5, 1, q, 3, q, 1, 5, 1, q, 2, 5],
    [5, 2, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 2, 5],
    [5, q, q, q, q, q, q, q, q, q, q, q, q, q, q, 5],
    [2, q, q, q, q, q, q, q, 6, q, q, q, q, q, q, 2],
    [2, q, q, 5, q, q, q, q, q, q, q, q, q, q, q, 5],
    [5, q, q, 2, q, q, q, q, q, q, 5, q, q, 3, q, 2],
    [2, q, q, 5, 2, 2, 5, q, q, q, 2, 2, 5, 2, 5, 5],
    [5, q, q, q, q, q, q, q, q, q, q, q, q, q, 6, 5],
    [2, q, q, q, q, q, q, q, 1, q, q, q, q, q, q, 4],
    [2, q, q, q, q, q, q, q, q, q, q, q, q, q, 6, 5],
    [2, q, q, 2, 5, 2, 5, q, q, q, 5, 2, 5, 2, 5, 5],
    [5, q, q, q, q, q, 5, q, q, q, 5, q, q, q, q, 2],
    [5, q, q, q, q, q, 2, q, 6, q, q, q, q, q, q, 5],
    [2, q, q, q, q, q, q, q, q, q, q, q, q, q, q, 2],
    [5, q, q, q, q, q, q, q, q, q, q, q, q, q, q, 2],
    [5, 2, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 5, 5],
    [5, 5, q, 1, 5, 5, 1, q, 3, q, 1, 5, 1, q, 2, 5],
    [5, 5, q, 3, 1, 1, 3, q, q, q, 3, 1, 3, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 2, 5],
    [5, 5, q, q, 2, 6, 5, q, q, q, 2, 6, q, q, 5, 5],
    [5, 2, q, q, q, q, q, q, q, q, q, q, q, q, 5, 5],
    [5, 5, q, q, q, q, q, q, 6, q, q, q, q, q, 2, 5],
    [5, 5, 2, 5, 5, 2, 5, 2, 5, 5, 2, 2, 5, 5, 5, 5]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 20)
         for pos in self.world_map]
