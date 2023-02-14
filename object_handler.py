from sprite_object import *
from nps import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.nps_list = []
        self.nps_sprite_path = 'resources/sprites/nps'
        self.static_sprite_path = 'resources/sprites/static_sprites'
        self.anim_sprite_path = 'resources/sprites/animated_sprite'
        add_sprite = self.add_sprite
        add_nps = self.add_nps
        self.nps_position = {}

        add_sprite(SpriteObject(game))
        add_sprite(SpriteObject(game, pos=(7.5, 1.5)))
        add_sprite(SpriteObject(game, pos=(2.5, 1.5)))
        add_sprite(SpriteObject(game, pos=(13.5, 1.5)))
        add_sprite(SpriteObject(game, pos=(8.5, 6.5)))
        add_sprite(SpriteObject(game, pos=(7.5, 29.5)))
        add_sprite(SpriteObject(game, pos=(9.5, 29.5)))
        add_sprite(SpriteObject(game, pos=(2.5, 29.5)))
        add_sprite(SpriteObject(game, pos=(8.5, 24.5)))
        add_sprite(SpriteObject(game, pos=(13.5, 29.5)))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(13.7, 14.5)))
        add_sprite(AnimatedSprite(game, pos=(13.7, 16.5)))
        add_sprite(AnimatedSprite(game, pos=(12.2, 14.5)))
        add_sprite(AnimatedSprite(game, pos=(12.2, 16.5)))
        add_sprite(AnimatedSprite(game, pos=(10.7, 14.5)))
        add_sprite(AnimatedSprite(game, pos=(10.7, 16.5)))

        add_sprite(AnimatedSprite(game, pos=(14.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 21.5)))
        add_sprite(AnimatedSprite(game, pos=(11.5, 18.5)))

        add_sprite(AnimatedSprite(game, pos=(14.5, 9.5)))
        add_sprite(AnimatedSprite(game, pos=(11.5, 12.5)))

        add_sprite(AnimatedSprite(game, pos=(1.5, 21.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 9.5)))

        add_nps(NPS(game))
        add_nps(NPS(game, pos=(9.5, 1.5)))
        add_nps(NPS(game, pos=(13.5, 1.5)))
        add_nps(NPS(game, pos=(9.6, 1.6)))
        add_nps(NPS(game, pos=(9.7, 1.7)))
        add_nps(NPS(game, pos=(13, 14.5)))
        add_nps(NPS(game, pos=(13.5, 29.5)))
        add_nps(NPS(game, pos=(8.5, 24.5)))
        add_nps(NPS(game, pos=(8.6, 24.6)))
        add_nps(NPS(game, pos=(7.5, 29.5)))
        add_nps(NPS(game, pos=(7.7, 29.7)))

    def update(self):
        self.nps_position = {nps.map_pos for nps in self.nps_list if nps.alive}
        [sprite.update() for sprite in self.sprite_list]
        [nps.update() for nps in self.nps_list]

    def add_nps(self, nps):
        self.nps_list.append(nps)

    def check_win(self):
        if not len(self.nps_position) and 14.0 < self.game.player.pos[0] < 15:
            self.game.object_render.game_win()

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)