import pygame
from interface import Interface
from physics import Physics


class Main(object):
    def __init__(self):
        self.running = True
        self.in_game = True
        self.in_death_screen = False
        self.in_menu = False
        self.in_score_screen = False
        self.in_text_input = False
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.interface = Interface()
        self.physics = Physics()

    def main_loop(self):
        while self.running:
            if self.in_menu:
                self.menu()
            if self.in_game:
                self.game_loop()
            if self.in_death_screen:
                self.death_screen()
            if self.in_score_screen:
                self.score_screen()
            if self.in_text_input:
                self.text_input()

        pygame.quit()

    def game_loop(self):
        self.clock.tick(self.FPS)
        self.interface.interface_loop(self.physics)
        self.physics.physics_loop(self.interface)
        if self.interface.high_score < self.physics.score:
            self.interface.high_score = self.physics.score
        if self.interface.keyboard_interrupt:
            self.running = False
        if self.interface.collided:
            self.in_game = False
            self.interface.collided = False
            self.in_death_screen = True
        pygame.display.update()

    def menu(self):
        self.interface.display_elements(self.physics)
        self.interface.menu()
        if self.interface.keyboard_interrupt:
            self.running = False
        if self.interface.restart:
            self.interface.restart = False
            self.in_menu = False
            self.in_game = True
            self.reset()
        if self.in_game:
            self.game_loop()
        if self.interface.go_to_score_screen:
            self.interface.go_to_score_screen = False
            self.in_menu = False
            self.in_score_screen = True
        pygame.display.update()

    def score_screen(self):
        self.interface.display_elements(self.physics)
        self.interface.score_screen()
        if self.interface.keyboard_interrupt:
            self.running = False
        if self.interface.go_to_menu:
            self.in_score_screen = False
            self.in_menu = True
            self.interface.go_to_menu = False
        if self.interface.go_to_text_input:
            self.interface.go_to_text_input = False
            self.in_score_screen = False
            self.in_text_input = True

        pygame.display.update()

    def text_input(self):
        self.interface.input_box()
        if self.interface.keyboard_interrupt:
            self.running = False
        if self.interface.leave_text_input:
            self.in_score_screen = True
            self.in_text_input = False
            self.interface.leave_text_input = False

    def death_screen(self):
        self.interface.death_screen()
        if self.interface.keyboard_interrupt:
            self.running = False
        if self.interface.restart:
            self.interface.restart = False
            self.in_death_screen = False
            self.in_game = True
            self.reset()
        if self.interface.go_to_menu:
            self.interface.go_to_menu = False
            self.in_death_screen = False
            self.in_menu = True

        pygame.display.update()

    def reset(self):
        self.interface.pipes = []
        self.interface.movable_pipe_distance = 0
        self.physics.reset(self.interface)


if __name__ == '__main__':
    pygame.init()
    main = Main()

    main.interface.load_assets()
    main.interface.interface_setup()
    main.main_loop()
