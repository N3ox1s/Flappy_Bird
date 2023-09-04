import pygame
from interface import Interface
from physics import Physics


class Main(object):
    def __init__(self):
        self.running = True
        self.FPS = 60
        self.clock = pygame.time.Clock()

    def main_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            interface.interface_loop()
            if interface.keyboard_interrupt:
                self.running = False

            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main = Main()
    physics = Physics()
    interface = Interface()

    interface.load_assets()
    interface.interface_setup()
    main.main_loop()
