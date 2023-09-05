import pygame
import math
import random

class Interface(object):
    def __init__(self):
        self.width = 1280
        self.height = 512
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.keyboard_interrupt = False
        self.jumped = False
        self.movable_pipe_distance = 0
        self.pipes = []

    def interface_loop(self, physics):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.jumped = True

        for i in range(self.tiles_bg):
            self.screen.blit(self.bg_day, (i * self.bg_width + self.bg_scroll, 0))

        self.movable_pipe_distance -= 2

        if self.movable_pipe_distance <= 0:
            self.pipes.append(pipe())
            self.movable_pipe_distance = physics.pipe_distance
            self.pipes[-1].set_pipe_length(random.randint(175, self.height-137))

        for i in self.pipes:
            if abs(i.pipe_scroll) >= self.width + self.pipe_green.get_width() + 300:
                self.pipes.remove(i)
            i.move()
            self.screen.blit(self.pipe_green, (self.width + i.pipe_scroll, i.lower_pipe_length))
            self.screen.blit(pygame.transform.rotate(self.pipe_green, 180), (self.width + i.pipe_scroll, i.lower_pipe_length - i.pipe_gap - 320))

        for i in range(self.tiles_base):
            self.screen.blit(self.bg_base, (i * self.base_width + self.fg_scroll, 400))

        self.bg_scroll -= 1
        self.fg_scroll -= 2

        if abs(self.bg_scroll) > self.bg_width:
            self.bg_scroll = 0

        if abs(self.fg_scroll) > self.bg_width:
            self.fg_scroll = 0

        self.screen.blit(self.current_bird_sprite(), (self.width // 2, physics.pos_y))

    def current_bird_sprite(self):
        time = pygame.time.get_ticks() // 100
        if time % 3 == 0:
            return self.yellow_bird_1
        if time % 3 == 1:
            return self.yellow_bird_2
        if time % 3 == 2:
            return self.yellow_bird_3

    def load_assets(self):
        self.icon = pygame.image.load("Assets/favicon.ico")
        self.bg_day = pygame.image.load("Assets/sprites/background-day.png")
        self.bg_night = pygame.image.load("Assets/sprites/background-night.png")
        self.bg_base = pygame.image.load("Assets/sprites/base.png")
        self.yellow_bird_1 = pygame.image.load("Assets/sprites/yellowbird-upflap.png")
        self.yellow_bird_2 = pygame.image.load("Assets/sprites/yellowbird-midflap.png")
        self.yellow_bird_3 = pygame.image.load("Assets/sprites/yellowbird-downflap.png")
        self.pipe_green = pygame.image.load("Assets/sprites/pipe-green.png")

    def interface_setup(self):
        self.bg_width = self.bg_day.get_width()
        self.base_width = self.bg_base.get_width()
        self.bg_scroll = 0
        self.fg_scroll = 0
        self.tiles_bg = math.ceil(self.width / self.bg_width) + 1
        self.tiles_base = math.ceil(self.width / self.base_width) + 1

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Flappy Bird")


class pipe(object):
    def __init__(self):
        self.pipe_scroll = 0
        self.lower_pipe_length = 0
        self.pipe_gap = random.randint(120, 200)

    def move(self):
        self.pipe_scroll -= 2

    def set_pipe_length(self, lower_pipe_length):
        self.lower_pipe_length = lower_pipe_length

