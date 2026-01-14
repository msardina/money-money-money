import pygame
from pygame import mixer
import os
import time

pygame.init()
mixer.init()

# begin
money = 0
income = 1
# setup font
extra_small_font = pygame.font.SysFont("comicsans", 20, True)
small_font = pygame.font.SysFont("comicsans", 45, True)
medium_font = pygame.font.SysFont("comicsans", 50, True)
big_font = pygame.font.SysFont("comicsans", 70, True)

# load images
dollar_img = pygame.image.load(os.path.join("assets", "dollar.svg"))
base_button_img = pygame.image.load(os.path.join("assets", "base_button.svg"))

# colors
WHITE = (255, 255, 255)
# setup a clock
clock = pygame.time.Clock()
FPS = 60

# setup screen
WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MONEY MONEY MONEY")


# class
class Button:
    def __init__(self, x, y, base_img, hover_base):
        self.clicked = False
        self.x = x
        self.y = y
        self.img = base_img
        self.hovering = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.normal_img = base_img
        self.hover_img = hover_base
        self.render = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, text):

        pos = pygame.mouse.get_pos()

        # Change State
        if self.rect.collidepoint(pos):
            self.hovering = True
        else:
            self.hovering = False
            self.clicked = False

        # Change Img using State
        self.img = self.hover_img if self.hovering else self.normal_img

        # Redo rect of button
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # if hovering, check if press
        if self.hovering:
            # left button clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        self.render = small_font.render(text, True, (0, 0, 0))
        screen.blit(self.img, (self.x, self.y))
        screen.blit(
            self.render,
            (
                self.x + self.img.get_width() / 2 - self.render.get_width() / 2,
                self.y + self.img.get_height() / 2 - self.render.get_height() / 2,
            ),
        )

    def is_clicked(self):
        return self.clicked


def game():
    # variables
    run = True
    global money
    global income

    # objects
    earn_button = Button(
        WIDTH / 2 - base_button_img.get_width() / 2,
        HEIGHT / 2,
        base_button_img,
        base_button_img,
    )
    # main loop
    while run:

        # loop through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit if x button pressed
                run = False
                pygame.quit()
                quit()
        # render text
        score_text = big_font.render(f"{money}", True, (0, 0, 0))
        income_text = extra_small_font.render(f"Income: +{income}", True, (0, 0, 0))
        # draw
        screen.fill(WHITE)
        screen.blit(
            dollar_img,
            (
                WIDTH / 2 - score_text.get_width() / 2 - dollar_img.get_width(),
                HEIGHT / 4 + 30,
            ),
        )
        screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 4))
        earn_button.update("Earn")
        screen.blit(
            income_text,
            (
                earn_button.x
                + base_button_img.get_width() / 2
                - income_text.get_width() / 2,
                earn_button.y + base_button_img.get_height(),
            ),
        )

        if earn_button.is_clicked():
            money += income
        # update
        pygame.display.update()
        clock.tick(FPS)


# run game

if __name__ == "__main__":
    game()
