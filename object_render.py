import pygame as pg
from settings import *


class ObjectRender:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_texture()
        self.sky_image = self.get_texture('resources/texture/sky.png', (WIGHT, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/texture/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_image = [self.get_texture(f'resources/texture/digits/{i}.png', [self.digit_size] * 2)
                            for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_image))
        self.scores = dict(zip(map(str, range(11)), self.digit_image))
        self.game_over_image = self.get_texture('resources/texture/game_over.png', RES)
        self.win_image = self.get_texture('resources/texture/win.png', RES)

    def draw(self):
        self.draw_backgroung()
        self.rander_game_objects()
        self.draw_player_health()
        self.draw_player_score()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def game_win(self):
        self.screen.blit(self.win_image, (0, 0))
        pg.display.flip()
        pg.mixer.music.stop()
        self.game.sound.win.play()
        pg.time.delay(10000)
        exit()

    def draw_player_score(self):
        score = str(self.game.player.score)
        for i, char in enumerate(score):
            self.screen.blit(self.scores[char], (i * self.digit_size + WIGHT - self.digit_size * 3, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_backgroung(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIGHT
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIGHT, 0))

        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIGHT, HEIGHT))

    def rander_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda x: x[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_texture(self):
        return {1: self.get_texture('resources/texture/1.png'),
                2: self.get_texture('resources/texture/2.png'),
                3: self.get_texture('resources/texture/3.png'),
                4: self.get_texture('resources/texture/4.png'),
                5: self.get_texture('resources/texture/5.png'),
                6: self.get_texture('resources/texture/6.png')
                }