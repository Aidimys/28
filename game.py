import random
import sys
import pygame
from pygame.locals import *  # noqa
from os import path
import time

pygame.font.init()
pygame.init()

pygame.display.set_caption("Flappy hell bird")

snd_dir = path.join(path.dirname(__file__), 'snd')
menumusic = pygame.mixer.Sound(path.join(snd_dir, "mm.mp3"))
menumusic.set_volume(0.3)
mainmusic = pygame.mixer.Sound(path.join(snd_dir, "doom.mp3"))
mainmusic.set_volume(0.5)
udarmusic = pygame.mixer.Sound(path.join(snd_dir, "udar.mp3"))
screen = pygame.display.set_mode((400, 708))
bg = pygame.image.load("PNG/bg2.jpg").convert()
bg_rect = bg.get_rect()

class Menu:
    def __init__(self, punkts=None):
        if punkts is None:
            punkts = [150, 200, u'Punkt', (255, 255, 255), (255, 0, 0), 0]
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.SysFont('Arial', 50)
        punkt = 0
        while done:
            screen.fill((0, 0, 0))
            screen.blit(bg, bg_rect)
            menumusic.play()

            pm = pygame.mouse.get_pos()
            for i in self.punkts:
                if i[0] < pm[0] < i[0] + 155 and i[1] < pm[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        sys.exit()
                    if e.type == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.type == pygame.K_DOWN:
                        if punkt < len(self.punkts):
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                        menumusic.stop()
                    elif punkt == 1:
                        sys.exit()

            screen.blit(screen, (0, 0))
            pygame.display.flip()


punkts = [(150, 200, u'Start', (50, 153, 168), (255, 0, 0), 0),
          (150, 300, u'Quit', (50, 153, 168), (255, 0, 0), 1)]

play = Menu(punkts)
play.menu()


class Replay:
    def __init__(self, punkts=None):
        if punkts is None:
            punkts = [150, 200, u'Punkt', (255, 255, 255), (255, 0, 0), 0]
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def rmenu(self):
        done = True
        font_menu = pygame.font.SysFont('Arial', 50)
        punkt = 0
        while done:
            screen.fill((0, 0, 0))
            screen.blit(bg, bg_rect)
            menumusic.play()

            pm = pygame.mouse.get_pos()
            for i in self.punkts:
                if i[0] < pm[0] < i[0] + 155 and i[1] < pm[1] < i[1] + 50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.type == pygame.K_ESCAPE:
                        sys.exit()
                    if e.type == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.type == pygame.K_DOWN:
                        if punkt < len(self.punkts):
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                        menumusic.stop()
                        FlappyFatBird().run()
                    elif punkt == 1:
                        sys.exit()

            screen.blit(screen, (0, 0))
            pygame.display.flip()


punkts = [(150, 200, u'Restart', (0, 255, 0), (255, 0, 0), 0),
          (150, 300, u'Quit', (0, 255, 0), (255, 0, 0), 1)]



class FlappyFatBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.bg = pygame.image.load("PNG/bg2.jpg").convert()
        self.birdsprite = [pygame.image.load("PNG/frame-1.png").convert(),
                           pygame.image.load("PNG/frame-2.png").convert(),
                           pygame.image.load("PNG/frame-death.png").convert(),
                           ]
        self.birdsprite[0].set_colorkey((255, 255, 255))
        self.birdsprite[1].set_colorkey((255, 255, 255))
        self.birdsprite[2].set_colorkey((255, 255, 255))
        self.wallUp = pygame.image.load("PNG/bottom.png").convert()
        self.wallDown = pygame.image.load("PNG/top.png").convert()
        self.gap = 130
        self.wallx = 400
        self.birdy = 350
        self.jump = 0
        self.gravity = 5
        self.jumpspeed = 10
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-100, 200)

    def WallUpdate(self):
        self.wallx -= 5
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 150)

    def BirdUpdate(self):
        if self.jump:
            self.jumpspeed -= 1
            self.birdy -= self.jumpspeed
            self.jump -= 1
        else:
            self.birdy += self.gravity
            self.gravity += 0.2
            self.bird[1] = self.birdy
            uprect = pygame.Rect(self.wallx, 360 + self.gap - self.offset + 10,
                                 self.wallUp.get_width() - 10,
                                 self.wallUp.get_height())
            downrect = pygame.Rect(self.wallx, 0 - self.gap - self.offset - 10,
                                   self.wallDown.get_width() - 10,
                                   self.wallDown.get_height())
            if uprect.colliderect(self.bird):
                self.birdsprite = [2]
                mainmusic.stop()
                udarmusic.play()
                self.dead = True
                if self.dead == True:
                    time.sleep(0.5)
                    play = Replay(punkts)
                    play.rmenu()
            if downrect.colliderect(self.bird):
                self.birdsprite = [2]
                mainmusic.stop()
                udarmusic.play()
                self.dead = True
                if self.dead == True:
                    time.sleep(0.5)
                    play = Replay(punkts)
                    play.rmenu()
            if not 0 < self.bird[1] < 700:
                mainmusic.stop()
                udarmusic.play()
                play = Replay(punkts)
                play.rmenu()
                self.bird[1] = 50
                self.birdy = 50
                self.dead = False
                self.counter = 0
                self.wallx = 400
                self.offset = random.randint(-110, 110)
                self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            mainmusic.play()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpspeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdsprite[self.sprite], (70, self.birdy))
            if not self.dead:
                self.sprite = 0
            if self.counter == 23:
                self.bg = pygame.image.load("PNG/bg.jpg").convert()
            if self.counter == 0:
                self.bg = pygame.image.load("PNG/bg2.jpg").convert()
            self.WallUpdate()
            self.BirdUpdate()
            pygame.display.update()


if __name__ == "__main__":
    FlappyFatBird().run()
