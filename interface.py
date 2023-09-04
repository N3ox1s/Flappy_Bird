import pygame
import math


class Interface(object):
    def __init__(self):
        self.width = 1280
        self.height = 512
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.keyboard_interrupt = False
        self.jumped = False

    def interface_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.jumped = True

        for i in range(0, self.tiles_bg):
            self.screen.blit(self.bg_day, (i * self.bg_width + self.bg_scroll, 0))

        for i in range(0, self.tiles_base):
            self.screen.blit(self.bg_base, (i * self.base_width + self.base_scroll, 400))

        self.bg_scroll -= 1
        self.base_scroll -= 2

        if abs(self.bg_scroll) > self.bg_width:
            self.bg_scroll = 0

        if abs(self.base_scroll) > self.bg_width:
            self.base_scroll = 0

    def load_assets(self):
        self.icon = pygame.image.load("Assets/favicon.ico")
        self.bg_day = pygame.image.load("Assets/sprites/background-day.png")
        self.bg_night = pygame.image.load("Assets/sprites/background-night.png")
        self.bg_base = pygame.image.load("Assets/sprites/base.png")

    def interface_setup(self):
        self.bg_width = self.bg_day.get_width()
        self.base_width = self.bg_base.get_width()
        self.bg_scroll = 0
        self.base_scroll = 0
        self.tiles_bg = math.ceil(self.width / self.bg_width) + 1
        self.tiles_base = math.ceil(self.width / self.base_width) + 1

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Flappy Bird")
        self.screen.blit(self.bg_day, (0, 0))
        self.screen.blit(self.bg_base, (0, 400))

