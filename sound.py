import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound'
        self.shotgun = pg.mixer.Sound(self.path + '/shotgun.mp3')
        self.nps_pain = pg.mixer.Sound(self.path + '/nps_pain.mp3')
        self.nps_death = pg.mixer.Sound(self.path + '/nps_death.mp3')
        self.nps_shot = pg.mixer.Sound(self.path + '/nps_attack.mp3')
        self.player_pain = pg.mixer.Sound(self.path + '/player_pain.mp3')
        self.win = pg.mixer.Sound(self.path + '/jojo_win.mp3')
        self.theme = pg.mixer.music.load(self.path + '/theme.mp3')
        self.nps_shot.set_volume(0.8)
        pg.mixer.music.set_volume(0.4)
