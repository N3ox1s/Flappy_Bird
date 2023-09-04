import pygame
from interface import Interface
from physics import Physics


class Main(object):
    def __init__(self):
        self.running = True
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.interface = Interface()
        self.physics = Physics(self.interface)

    def main_loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.interface.interface_loop()
            if self.interface.keyboard_interrupt:
                self.running = False
            self.physics.physics_loop()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main = Main()

    main.interface.load_assets()
    main.interface.interface_setup()
    main.main_loop()
