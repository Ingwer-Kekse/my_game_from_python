from settings import *
from main import *
import pygame as pg
import os


class Okno:
    def __init__(self):
        pg.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pg.display.set_mode(RES)
        self.font = "other/text.ttf"
        self.first_image = pg.image.load('resources/texture/doom_image.png')
        self.clock = pg.time.Clock()

    def main_menu(self):

        menu = True
        selected = "start"

        while menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        selected = "start"
                    elif event.key == pg.K_DOWN:
                        selected = "quit"
                    if event.key == pg.K_RETURN:
                        if selected == "start":
                            game = Game()
                            game.run()
                        if selected == "quit":
                            pg.quit()
                            quit()

            self.screen.blit(self.first_image, (0, 0))
            if selected == "start":
                text_start = self.text_format("START", self.font, 75, (242, 0, 0))
            else:
                text_start = self.text_format("START", self.font, 75, (140, 0, 0))
            if selected == "quit":
                text_quit = self.text_format("QUIT", self.font, 75, (242, 0, 0))
            else:
                text_quit = self.text_format("QUIT", self.font, 75, (140, 0, 0))

            start_rect = text_start.get_rect()
            quit_rect = text_quit.get_rect()

            self.screen.blit(text_start, (WIGHT // 2 - (start_rect[2]/2), 430))
            self.screen.blit(text_quit, (WIGHT // 2 - (quit_rect[2]/2), 560))
            pg.display.update()
            self.clock.tick(FPS)
            pg.display.set_caption("My DOOM")

    def text_format(self, message, textFont, textSize, textColor):
        newFont = pg.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText


if __name__ == '__main__':
    okno = Okno()
    okno.main_menu()