import pygame
from interface import Interface
from physics import Physics


class Main(object):
    def __init__(self):
        self.running = True

    def main_loop(self):
        while self.running:
            interface.interface_loop()
            if interface.keyboard_interrupt:
                self.running = False

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    main = Main()
    physics = Physics()
    interface = Interface()

    interface.load_assets()
    main.main_loop()
