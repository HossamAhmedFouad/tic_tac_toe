import pygame
import os
from menu import *

# Getting current directory that the project is currently in
cwd = os.getcwd()


# Game Class that holds game attributes


class Game(object):
    # on initialization declare following attributes
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT = 600, 800
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.window = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.left_Click, self.right_Click = False, False
        self.mx, self.my = 0, 0
        self.soundsOn = True
        self.main_menu = MainMenu(self)
        self.start = StartMenu(self)
        self.optionsMenu = Options(self)
        self.creditsMenu = Credits(self)
        self.curr_menu = self.main_menu

    # Game loop which monitors main controls and keyboard inputs
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    # The function that checks for any possible event done by the player

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_Click = True
                    self.mx, self.my = pygame.mouse.get_pos()

    # resetting keys detection to wait for another detection
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.left_Click = False, False, False, False, False

    # adds text to screen with x and y positions
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    # draws lines on the screen
    def draw_lines(self, screen, color, tupleStartX_Y, tupleEndX_Y, lineWidth):
        line = pygame.draw.line(screen, color, tupleStartX_Y, tupleEndX_Y, lineWidth)
        pygame.display.update()

    # add images on screen
    def add_Images(self, image, posX, posY):
        number = pygame.image.load(f"{cwd}\Assets\\numbers\\{image}.png")
        number = pygame.transform.scale(number, (50, 50))
        self.display.blit(number, (posX, posY))
