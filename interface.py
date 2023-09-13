import pygame
import math
import random
from pipe import Pipe


class Interface(object):
    def __init__(self):
        self.width = 1280
        self.height = 512
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.keyboard_interrupt = False
        self.jumped = False
        self.collided = False
        self.restart = False
        self.go_to_menu = False
        self.go_to_score_screen = False
        self.go_to_text_input = False
        self.movable_pipe_distance = 0
        self.pipes = []
        self.pipe_skins = []
        self.pipe_colliders = []
        self.bird_collider = None
        self.ground_collider = None
        self.leave_text_input = False
        self.text = ""
        self.bg_scroll = 0
        self.fg_scroll = 0
        self.highscore_list = []
        self.score = 0

    def interface_loop(self, physics):

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.jumped = True

        # calculate scroll of elements on screen
        self.scroll(physics)

        # Screen refresh
        self.display_elements(physics)

        # check for collisions
        self.collider(physics)

    def scroll(self, physics):

        # Movement of Elements
        if self.movable_pipe_distance <= 0:
            self.pipes.append(Pipe())
            self.movable_pipe_distance = physics.pipe_distance
            self.pipes[-1].set_pipe_length(random.randint(175, self.height - 137))
            self.pipes[-1].set_pipe_skin(self.current_pipe_skin)

        self.movable_pipe_distance -= 2

        for i in self.pipes:
            if abs(i.pipe_scroll) >= self.width + 500:
                self.pipes.remove(i)
            i.move()

        self.bg_scroll -= 1
        self.fg_scroll -= 2

        if abs(self.bg_scroll) > self.bg_width:
            self.bg_scroll = 0

        if abs(self.fg_scroll) > self.bg_width:
            self.fg_scroll = 0

    def collider(self, physics):
        # Collider
        self.ground_collider = pygame.Rect(0, 400, self.width, self.height)

        self.pipe_colliders = []
        for i in self.pipes:
            self.pipe_colliders.append(
                pygame.Rect(self.width + i.pipe_scroll, i.lower_pipe_length, self.current_pipe_skin.get_width(),
                            self.current_pipe_skin.get_height()))
            self.pipe_colliders.append(pygame.Rect(self.width + i.pipe_scroll, 0,
                                                   self.current_pipe_skin.get_width(),
                                                   i.lower_pipe_length - i.pipe_gap))

        self.bird_collider = pygame.Rect(self.width / 2, physics.pos_y, self.current_bird_sprite().get_width(),
                                         self.current_bird_sprite().get_height())

        for i in self.pipe_colliders:
            if i.colliderect(self.bird_collider):
                self.collided = True
        if self.ground_collider.colliderect(self.bird_collider):
            self.collided = True

    def display_elements(self, physics):
        for i in range(self.tiles_bg):
            self.screen.blit(self.bg_day, (i * self.bg_width + self.bg_scroll, 0))

        for i in self.pipes:
            self.screen.blit(i.pipe_image, (self.width + i.pipe_scroll, i.lower_pipe_length))
            self.screen.blit(pygame.transform.rotate(i.pipe_image, 180),
                             (self.width + i.pipe_scroll, i.lower_pipe_length - i.pipe_gap - 320))

        for i in range(self.tiles_base):
            self.screen.blit(self.bg_base, (i * self.base_width + self.fg_scroll, 400))

        self.screen.blit(self.current_bird_sprite(), (self.width // 2, physics.pos_y))

        self.score = str(physics.score)
        self.screen.blit(self.font.render(self.score, True, (255, 255, 255)), (100, 80))

        self.screen.blit(pygame.transform.scale(self.pokal, (50, 50)), (30, 20))
        self.screen.blit(self.font.render(str(self.high_score), True, (255, 255, 255)), (100, 20))

    def menu(self):
        logo = pygame.transform.scale(self.logo, (
            self.logo.get_width() * 3, self.logo.get_height() * 3))
        self.screen.blit(logo, (500, 100))
        play_button = pygame.transform.scale(self.play_button, (
            self.play_button.get_width() * 5, self.play_button.get_height() * 5))
        self.screen.blit(play_button, (720, 204))
        exit_button = pygame.transform.scale(self.exit_button, (
            self.exit_button.get_width() * 5, self.exit_button.get_height() * 5))
        self.screen.blit(exit_button, (720, 284))
        skin_button = pygame.transform.scale(self.skin_button, (
            self.skin_button.get_width() * 5, self.skin_button.get_height() * 5))
        self.screen.blit(skin_button, (490, 200))
        score_button = pygame.transform.scale(self.score_button, (
            self.score_button.get_width() * 5, self.score_button.get_height() * 5))
        self.screen.blit(score_button, (490, 280))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        exit_button_dim = (720, 720 + play_button.get_width(), 284, 284 + play_button.get_height())
        if (exit_button_dim[0] < mouse[0] < exit_button_dim[1] and exit_button_dim[2] < mouse[1] < exit_button_dim[3]
                and click):
            self.keyboard_interrupt = True
        play_button_dim = (720, 720 + play_button.get_width(), 200, 200 + play_button.get_height())
        if (play_button_dim[0] < mouse[0] < play_button_dim[1] and play_button_dim[2] < mouse[1] < play_button_dim[3]
                and click):
            self.restart = True
        score_button_dim = (490, 490 + score_button.get_width(), 280, 280 + score_button.get_height())
        if (score_button_dim[0] < mouse[0] < score_button_dim[1] and score_button_dim[2] < mouse[1] < score_button_dim[
            3]
                and click):
            self.go_to_score_screen = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True

    def score_screen(self):
        score_board = pygame.transform.scale(self.score_board, (
            self.score_board.get_width() * 5, self.score_board.get_height() * 5))
        self.screen.blit(score_board, (490, 20))
        back_button = pygame.transform.scale(self.back_button, (
            self.back_button.get_width() * 5, self.back_button.get_height() * 5))
        self.screen.blit(back_button, (410, 400))
        input_button = pygame.transform.scale(self.input_button, (
            self.input_button.get_width() * 5, self.input_button.get_height() * 5))
        self.screen.blit(input_button, (800, 320))

        self.text_surface = self.input_font.render(str(self.text), True, (85, 48, 6))
        self.screen.blit(self.text_surface, (825, 350))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]



        back_button_dim = (410, 410 + back_button.get_width(), 400, 400 + back_button.get_height())
        if (back_button_dim[0] < mouse[0] < back_button_dim[1] and back_button_dim[2] < mouse[1] < back_button_dim[3]
                and click):
            self.go_to_menu = True
            self.in_text_input = False

        self.input_button_dim = (800, 800 + input_button.get_width(), 320, 320 + input_button.get_height())
        if (self.input_button_dim[0] < mouse[0] < self.input_button_dim[1] and self.input_button_dim[2] < mouse[1] <
                self.input_button_dim[3]
                and click):
            self.go_to_text_input = True
            self.input_box()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True

    def input_box(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True

            if pygame.key.get_pressed()[pygame.K_RETURN]:
                self.leave_text_input = True
                self.highscore_list.append([self.text, self.score])
                with open("highscores.txt", "a") as file:
                    file.write(self.text + " " + self.score + "\n")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    if self.text_surface.get_width() > self.input_button.get_width() * 5 - 65:
                        self.text = self.text[:-1]

        if not (self.input_button_dim[0] < mouse[0] < self.input_button_dim[1] and self.input_button_dim[2] < mouse[1] <
                self.input_button_dim[3]) and click:
            self.leave_text_input = True

        pygame.draw.rect(self.screen, (255, 247, 216), (819, 339, 172, 37))
        self.text_surface = self.input_font.render(str(self.text), True, (85, 48, 6))
        self.screen.blit(self.text_surface, (825, 350))
        pygame.display.flip()

    def death_screen(self):
        menu_button = pygame.transform.scale(self.menu_button, (
            self.menu_button.get_width() * 5, self.menu_button.get_height() * 5))
        self.screen.blit(menu_button, (490, 200))
        play_button = pygame.transform.scale(self.play_button, (
            self.play_button.get_width() * 5, self.play_button.get_height() * 5))
        self.screen.blit(play_button, (720, 204))
        game_over = pygame.transform.scale(self.game_over, (
            self.game_over.get_width() * 1.5, self.game_over.get_height() * 1.5))
        self.screen.blit(game_over, (500, 100))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        menu_button_dim = (490, 490 + menu_button.get_width(), 200, 200 + menu_button.get_height())
        if (menu_button_dim[0] < mouse[0] < menu_button_dim[1] and menu_button_dim[2] < mouse[1] < menu_button_dim[3]
                and click):
            self.go_to_menu = True
        play_button_dim = (720, 720 + play_button.get_width(), 200, 200 + play_button.get_height())
        if (play_button_dim[0] < mouse[0] < play_button_dim[1] and play_button_dim[2] < mouse[1] < play_button_dim[3]
                and click):
            self.restart = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keyboard_interrupt = True

    def current_bird_sprite(self):
        time = pygame.time.get_ticks() // 100
        if time % 3 == 0:
            return self.yellow_bird_1
        if time % 3 == 1:
            return self.yellow_bird_2
        if time % 3 == 2:
            return self.yellow_bird_3

    def load_assets(self):
        self.pokal = pygame.image.load("Assets/sprites/pokal.png")
        self.icon = pygame.image.load("Assets/favicon.ico")
        self.game_over = pygame.image.load("Assets/sprites/gameover.png")
        self.menu_button = pygame.image.load("Assets/sprites/menu-button.png")
        self.play_button = pygame.image.load("Assets/sprites/play-button.png")
        self.exit_button = pygame.image.load("Assets/sprites/exit-button.png")
        self.score_board = pygame.image.load("Assets/sprites/score-board.png")
        self.skin_menu = pygame.image.load("Assets/sprites/skin-menu.png")
        self.back_button = pygame.image.load("Assets/sprites/back-button.png")
        self.bg_day = pygame.image.load("Assets/sprites/background-day.png")
        self.bg_night = pygame.image.load("Assets/sprites/background-night.png")
        self.bg_base = pygame.image.load("Assets/sprites/base.png")
        self.logo = pygame.image.load("Assets/sprites/logo.png")
        self.skin_button = pygame.image.load("Assets/sprites/skins-button.png")
        self.score_button = pygame.image.load("Assets/sprites/score-button.png")
        self.yellow_bird_1 = pygame.image.load("Assets/sprites/yellowbird-upflap.png")
        self.yellow_bird_2 = pygame.image.load("Assets/sprites/yellowbird-midflap.png")
        self.yellow_bird_3 = pygame.image.load("Assets/sprites/yellowbird-downflap.png")
        self.pipe_skin_green = pygame.image.load("Assets/sprites/pipe-green.png")
        self.pipe_skin_red = pygame.image.load("Assets/sprites/pipe-red.png")
        self.font = pygame.font.Font("Assets/font/flappy-bird-font.ttf", 50)
        self.input_font = pygame.font.Font("Assets/font/flappy-bird-font.ttf", 25)
        self.input_button = pygame.image.load("Assets/sprites/input-button.png")
        self.current_pipe_skin = self.pipe_skin_green

        with open("Highscores.txt") as file:
            for line in file:
                self.highscore_list.append(line.split())

        print(self.highscore_list)

    def interface_setup(self):
        self.bg_width = self.bg_day.get_width()
        self.base_width = self.bg_base.get_width()
        self.tiles_bg = math.ceil(self.width / self.bg_width) + 1
        self.tiles_base = math.ceil(self.width / self.base_width) + 1

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Flappy Bird")
