import pygame


class Interface(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.keyboard_interrupt = False

    def interface_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True

    def load_assets(self):
        pygame.display.set_icon(pygame.image.load("Assets/favicon.ico"))
