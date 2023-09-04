import pygame
import math


class Interface(object):
    def __init__(self):
        self.width = 1280
        self.height = 512
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.keyboard_interrupt = False

    def interface_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True

    def load_assets(self):
        self.icon = pygame.image.load("Assets/favicon.ico")
        self.bg_day = pygame.image.load("Assets/sprites/background-day.png")
        self.bg_night = pygame.image.load("Assets/sprites/background-night.png")
        self.bg_base = pygame.image.load("Assets/sprites/base.png")


    def interface_setup(self):
        bg_width = self.bg_day.get_width()

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Flappy Bird")
        self.screen.blit(self.bg_day, (0, 0))
        self.screen.blit(self.bg_base, (0, 400))

