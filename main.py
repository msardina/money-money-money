import pygame
from pygame import mixer
import os
import time
import random

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

ALL_BARS = ["Shop", "Job", "Casino"]
TITLE_TEXT = [
    small_font.render(text_content, True, (0, 0, 0)) for text_content in ALL_BARS
]


# load images
dollar_img = pygame.image.load(os.path.join("assets", "dollar.svg"))
base_button_img = pygame.image.load(os.path.join("assets", "base_button.svg"))

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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


def draw_text_bar(title_text, ypos, state, screen):
    # boarder
    pygame.draw.line(screen, BLACK, (0, 0), (0, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (WIDTH - 2.5, 0), (WIDTH - 2.5, HEIGHT), 5)
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 2.5), (WIDTH, HEIGHT - 2.5), 5)
    pygame.draw.line(screen, BLACK, (0, 0), (WIDTH, 0), 5)
    pygame.draw.line(screen, BLACK, (0, ypos), (WIDTH, ypos), 5)
    block_width = WIDTH / (len(title_text))
    new_state = state
    for i, text in enumerate(title_text):
        rect = pygame.Rect(block_width * i, 0, block_width, ypos)
        # draw text and line
        screen.blit(
            text, ((block_width * i + block_width / 2) - text.get_width() / 2, -12)
        )
        pygame.draw.line(
            screen, BLACK, (block_width * i, 0), (block_width * i, ypos), 5
        )

        # draw white part
        if ALL_BARS[i] == state:
            pygame.draw.line(
                screen,
                WHITE,
                (block_width * i + 2.5, ypos),
                (block_width * (i + 1) - 2.5, ypos),
                5,
            )

        # check for click
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            new_state = ALL_BARS[i]

    return new_state


def draw_job(earn_button):
    global money
    # render text
    score_text = big_font.render(f"{money}", True, (0, 0, 0))
    income_text = extra_small_font.render(f"Income: +{income}", True, (0, 0, 0))

    # draw
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

    # check for button click
    if earn_button.is_clicked():
        money += income


def draw_casino(bet_button, numbers, betting, amount, win_loss_text):

    # draw boxes
    box_width = 100
    for i in range(1, 4):
        pygame.draw.rect(
            screen,
            BLACK,
            (box_width * i, HEIGHT / 4, box_width, box_width),
            5,
        )
    # draw numbers
    for i, number in enumerate(numbers):
        number_text = big_font.render(number, True, (0, 0, 0))
        screen.blit(
            number_text,
            (
                box_width * (i + 1) + box_width / 2 - number_text.get_width() / 2,
                HEIGHT / 4,
            ),
        )
    # draw buttons
    bet_button.update("Bet")

    # enter money amount
    amount_text = medium_font.render(amount, True, (0, 0, 0))
    win_loss = extra_small_font.render(win_loss_text, True, (0, 0, 0))
    screen.blit(
        amount_text,
        (
            WIDTH / 2 - amount_text.get_width() / 2,
            HEIGHT / 2 - amount_text.get_height() - 10,
        ),
    )
    screen.blit(
        dollar_img,
        (
            WIDTH / 2 - amount_text.get_width() / 2 - 35,
            HEIGHT / 2 - amount_text.get_height(),
        ),
    )
    screen.blit(
        win_loss, (bet_button.x, bet_button.y + base_button_img.get_height() + 2)
    )
    # random bet

    if bet_button.is_clicked() and not betting:
        betting = True
    if betting:
        for i in range(0, len(numbers)):
            numbers[i] = str(random.randint(0, 9))

    # check for victory
    return betting, numbers


def main():
    # variables
    run = True
    state = "Job"
    global money
    global income
    numbers = ["0", "0", "0"]
    betting = False
    bet_timer = 0
    bet_amount = "100"
    win_loss_text = "make a bet!"
    # objects
    earn_button = Button(
        WIDTH / 2 - base_button_img.get_width() / 2,
        HEIGHT / 2,
        base_button_img,
        base_button_img,
    )
    bet_button = Button(
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

            if event.type == pygame.TEXTINPUT:

                if event.text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    bet_amount += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    bet_amount = bet_amount[:-1]

        # draw
        screen.fill(WHITE)
        if state == "Job":
            draw_job(earn_button)
        if state == "Casino":
            betting_numbers = draw_casino(
                bet_button, numbers, betting, bet_amount, win_loss_text
            )
            betting = betting_numbers[0]
            numbers = betting_numbers[1]

        if betting:
            bet_timer += 0.010
        if bet_timer > 2:
            betting = False
            bet_timer = 0
            unique_numbers = set(numbers)
            # check victory
            if len(unique_numbers) != len(numbers):
                money -= int(bet_amount)
                money += int(bet_amount) * 3
                win_loss_text = "Lucky! x3"
            elif numbers[0] == numbers[1] == numbers[2]:
                money -= int(bet_amount)
                money += int(bet_amount) * 21
                win_loss_text = "ARE U HACKING? x21"
            else:
                money -= int(bet_amount)
                win_loss_text = "Oopsies. Try again. Sorry!"

        # draw tpo bar
        state = draw_text_bar(TITLE_TEXT, 55, state, screen)

        # update
        pygame.display.update()
        clock.tick(FPS)


# run game

if __name__ == "__main__":
    main()
