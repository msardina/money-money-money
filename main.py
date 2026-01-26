import pygame
from pygame import mixer
import os
import time
import random
import math

pygame.init()
mixer.init()
# sounds
click_sfx = pygame.mixer.Sound(os.path.join("sounds", "click.wav"))
lofi = pygame.mixer.Sound(os.path.join("sounds", "lofi_music.mp3"))
lofi.play(-1)
# begin
money = 0
income = 1
# setup font
EXTRA_SMALL_FONT = pygame.font.SysFont("comicsans", 20, True)
SMALL_FONT = pygame.font.SysFont("comicsans", 45, True)
MEDIUM_FONT = pygame.font.SysFont("comicsans", 50, True)
BIG_FONT = pygame.font.SysFont("comicsans", 70, True)

ALL_BARS = ["Shop", "Job", "Casino"]
TITLE_TEXT = [
    SMALL_FONT.render(text_content, True, (0, 0, 0)) for text_content in ALL_BARS
]

# income dic
INCOME_RARITY = {0: 4, 1: 10, 2: 50, 3: 150, 4: 500, 5: 1000}
RARITY_BOUNCE = {0: 50, 1: 100, 2: 1500, 3: 100000, 4: 100000, 5: 1000000}
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# setup a clock
clock = pygame.time.Clock()
FPS = 60

# setup screen
og_width, og_height = 500, 800
screen_width, screen_height = og_width, og_height
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("MONEY MONEY MONEY")

# load images
shop_egg = pygame.image.load(os.path.join("assets", "lucky_egg.svg"))
dollar_img = pygame.image.load(os.path.join("assets", "dollar.svg"))
base_button_img = pygame.image.load(os.path.join("assets", "base_button.svg"))
base_button_hover_img = pygame.image.load(
    os.path.join("assets", "base_button_hover.svg")
)
loot_table = pygame.image.load(os.path.join("assets", "loot_table.png"))
loot_table = pygame.transform.scale(loot_table, (screen_width, loot_table.get_height()))

RARITIES = ["rare", "super_rare", "epic", "mythic", "legendary", "chromatic"]
egg_imgs = []
egg_imgs_back = []
blob_imgs = []
card_imgs = []
for rarity in RARITIES:
    egg_imgs.append(pygame.image.load(os.path.join("assets", "eggs", f"{rarity}.svg")))
    egg_imgs_back.append(
        pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "eggs", f"{rarity}_backdrop.svg")),
            (screen_width, screen_height),
        )
    )
    card_imgs.append(
        pygame.image.load(os.path.join("assets", "cards", f"{rarity}_card.png"))
    )

for rarity in RARITIES:
    img = pygame.image.load(os.path.join("assets", "blobs", f"{rarity}_blob.svg"))
    blob_imgs.append(
        pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
    )


# class
class Button:
    def __init__(self, x, y, base_img, hover_base, is_continues):
        self.continues = is_continues
        self.x = x
        self.y = y
        self.img = base_img
        self.hovering = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.normal_img = base_img
        self.hover_img = hover_base
        self.text = ""
        self.render = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.enabled = True
        self.clicked = True  # was clicked in last cycle

    def update_status(self):
        # Change State
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovering = True
        else:
            self.hovering = False

        pressed = pygame.mouse.get_pressed()[0] == 1
        self.clicked = (
            (self.continues or not self.clicked)
            and self.hovering
            and pressed
            and self.enabled
        )
        if self.continues:
            self.enabled = True
        else:
            self.enabled = (
                not self.enabled and (not self.hovering or not pressed)
            ) or (self.enabled and not (self.hovering and pressed))

    def update(self, text, size_font, x, y):
        self.x = x
        self.y = y

        # status
        self.update_status()
        self.text = text

        # Change Img using State
        self.img = self.hover_img if self.hovering else self.normal_img

        # Redo rect of button
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # if hovering, check if press
        self.render = size_font.render(self.text, True, (0, 0, 0))
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


class Blob:
    def __init__(self, rarity_num, blob_imgs):
        self.rarity_num = rarity_num
        self.img = blob_imgs[rarity_num]
        self.x = random.randint(0, screen_width - self.img.get_width())
        self.y = screen_height - self.img.get_height()
        self.side = 1

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, screen_height):
        bounce = False
        self.x += self.side
        self.y = screen_height - self.img.get_height()
        if self.x < 0:
            self.side = self.side * -1
            bounce = True

        elif self.x > screen_width - self.img.get_width():
            self.side = self.side * -1
            bounce = True

        return bounce


def draw_egg_opening(rarity_num, chances_left):
    global egg_imgs_back
    # resize loot table
    egg_imgs_back = []
    for rarity in RARITIES:
        egg_imgs_back.append(
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "eggs", f"{rarity}_backdrop.svg")
                ),
                (screen_width, screen_height),
            )
        )
    screen.blit(egg_imgs_back[rarity_num], (0, 0))
    screen.blit(
        egg_imgs[rarity_num],
        (
            screen_width / 2 - egg_imgs[rarity_num].get_width() / 2,
            screen_height / 2 - egg_imgs[rarity_num].get_height() / 2,
        ),
    )
    rarity = RARITIES[rarity_num].upper()
    egg_rarity_text = BIG_FONT.render(f"{rarity.replace("_", " ")}", True, (0, 0, 0))
    screen.blit(
        egg_rarity_text, (screen_width / 2 - egg_rarity_text.get_width() / 2, 100)
    )
    tiny_img = pygame.transform.scale(egg_imgs[1], (60, 80))
    full_width = (tiny_img.get_width() + 15) * 5
    for i in range(0, chances_left - 1):

        tiny_img = pygame.transform.scale(egg_imgs[rarity_num], (60, 80))
        screen.blit(
            tiny_img,
            (
                (
                    (screen_width / 2 - full_width / 2)
                    + ((tiny_img.get_width() + 15)) * i
                ),
                screen_height - 100,
            ),
        )

    if chances_left == 1:
        tap_to_open = MEDIUM_FONT.render(f"TAP TO OPEN", True, (0, 0, 0))
        screen.blit(
            tap_to_open,
            (screen_width / 2 - tap_to_open.get_width() / 2, screen_height - 100),
        )


def draw_shop(buy_egg_button: Button, egg_price, money, screen_width, screen_height):

    # draw buy egg
    egg_price_text = MEDIUM_FONT.render(f"{egg_price}", True, (0, 0, 0))
    screen.blit(egg_price_text, (screen_width / 2 - egg_price_text.get_width() / 2, 90))
    screen.blit(
        loot_table,
        (
            screen_width / 2 - loot_table.get_width() / 2,
            screen_height - loot_table.get_height(),
        ),
    )
    # draw egg
    screen.blit(
        shop_egg,
        (
            screen_width / 2 - shop_egg.get_width() / 2,
            screen_height / 2 - shop_egg.get_height() / 2 - 100,
        ),
    )
    screen.blit(
        dollar_img,
        (
            screen_width / 2 - egg_price_text.get_width() / 2 - dollar_img.get_width(),
            100,
        ),
    )

    if egg_price <= money:
        buy_egg_button.update(
            "buy",
            MEDIUM_FONT,
            screen_width / 2 - base_button_img.get_width() / 2,
            screen_height / 1.7,
        )
        if buy_egg_button.is_clicked():
            return True
        else:
            return False
    else:
        buy_egg_button.update(
            "cant afford",
            EXTRA_SMALL_FONT,
            screen_width / 2 - base_button_img.get_width() / 2,
            screen_height / 1.7,
        )
        return False


def draw_text_bar(title_text, ypos, state, screen):
    # boarder
    pygame.draw.line(screen, BLACK, (0, 0), (0, screen_height), 5)
    pygame.draw.line(
        screen, BLACK, (screen_width - 2.5, 0), (screen_width - 2.5, screen_height), 5
    )
    pygame.draw.line(
        screen, BLACK, (0, screen_height - 2.5), (screen_width, screen_height - 2.5), 5
    )
    pygame.draw.line(screen, BLACK, (0, 0), (screen_width, 0), 5)
    pygame.draw.line(screen, BLACK, (0, ypos), (screen_width, ypos), 5)
    block_width = screen_width / (len(title_text))
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


def draw_job(
    earn_button, blobs, boost_button, boost_price, screen_width, screen_height
):
    global money
    global income
    # render text
    score_text = BIG_FONT.render(f"{money}", True, (0, 0, 0))
    boost_price_txt = EXTRA_SMALL_FONT.render(f"${boost_price}", True, (0, 0, 0))
    income_text = EXTRA_SMALL_FONT.render(f"Income: +{income}", True, (0, 0, 0))

    # bought
    bought = False
    # draw
    screen.blit(
        dollar_img,
        (
            screen_width / 2 - score_text.get_width() / 2 - dollar_img.get_width(),
            screen_height / 4 + 30,
        ),
    )
    screen.blit(
        score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 4)
    )
    earn_button.update(
        "Earn",
        MEDIUM_FONT,
        screen_width / 2 - base_button_img.get_width() / 2,
        screen_height / 2,
    )
    screen.blit(
        income_text,
        (
            earn_button.x
            + base_button_img.get_width() / 2
            - income_text.get_width() / 2,
            earn_button.y + base_button_img.get_height(),
        ),
    )
    screen.blit(
        boost_price_txt,
        (
            screen_width / 2 - boost_price_txt.get_width() / 2,
            boost_button.y + base_button_img.get_height() + 5,
        ),
    )
    if money > boost_price:
        boost_button.update(
            "Go to school",
            EXTRA_SMALL_FONT,
            screen_width / 2 - base_button_img.get_width() / 2,
            screen_height / 1.5,
        )
    else:
        boost_button.update(
            "cannot afford",
            EXTRA_SMALL_FONT,
            screen_width / 2 - base_button_img.get_width() / 2,
            screen_height / 1.5,
        )
    # check for button click
    if earn_button.is_clicked():
        money += income

    if boost_button.is_clicked() and money > boost_price:
        income *= 1.4
        income = math.ceil(income)
        bought = True
    # draw blobs

    for blob in blobs:
        blob.draw()
        if blob.move(screen_height):
            money += RARITY_BOUNCE[blob.rarity_num]

    return bought


def draw_casino(
    bet_button, numbers, betting, amount, win_loss_text, screen_width, screen_height
):

    # draw boxes
    box_width = 100
    full_width = box_width * 3
    box_start = screen_width / 2 - full_width / 2
    for i in range(0, 3):
        pygame.draw.rect(
            screen,
            BLACK,
            (box_start + box_width * i, screen_height / 4, box_width, box_width),
            5,
        )
    # draw numbers
    for i, number in enumerate(numbers):
        number_text = BIG_FONT.render(number, True, (0, 0, 0))
        screen.blit(
            number_text,
            (
                (box_start + box_width * i) + number_text.get_width() / 2,
                screen_height / 4,
            ),
        )
    # draw buttons
    bet_button.update(
        "Bet",
        MEDIUM_FONT,
        screen_width / 2 - base_button_img.get_width() / 2,
        screen_height / 2,
    )

    # enter money amount
    amount_text = MEDIUM_FONT.render(amount, True, (0, 0, 0))
    win_loss = EXTRA_SMALL_FONT.render(win_loss_text, True, (0, 0, 0))
    screen.blit(
        amount_text,
        (
            screen_width / 2 - amount_text.get_width() / 2,
            screen_height / 2 - amount_text.get_height() - 10,
        ),
    )
    screen.blit(
        dollar_img,
        (
            screen_width / 2 - amount_text.get_width() / 2 - 35,
            screen_height / 2 - amount_text.get_height(),
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
    global screen_width
    global screen_height
    numbers = ["0", "0", "0"]
    betting = False
    bet_timer = 0
    bet_amount = "100"
    win_loss_text = "make a bet!"
    egg_price = 100
    buying_egg = False
    rarity_num = 0
    open_chances = 6
    blobs = []
    boost_price = 100
    # objects
    earn_button = Button(
        screen_width / 2 - base_button_img.get_width() / 2,
        screen_height / 2,
        base_button_img,
        base_button_hover_img,
        True,
    )
    bet_button = Button(
        screen_width / 2 - base_button_img.get_width() / 2,
        screen_height / 2,
        base_button_img,
        base_button_hover_img,
        False,
    )
    buy_egg_button = Button(
        screen_width / 2 - base_button_img.get_width() / 2,
        screen_height / 1.7,
        base_button_img,
        base_button_hover_img,
        False,
    )
    boost_button = Button(
        screen_width / 2 - base_button_img.get_width() / 2,
        screen_height / 1.5,
        base_button_img,
        base_button_hover_img,
        False,
    )
    eggs_since_good_reward = 0
    # main loop
    while run:

        # resize screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        # loop through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit if x button pressed
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sfx.play()

            if state == "Egg Open":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if open_chances > 1:
                        if eggs_since_good_reward > 8:
                            rarity_num += 1
                        elif random.randint(0, 100) < 25:
                            rarity_num += 1
                    open_chances -= 1
            if event.type == pygame.TEXTINPUT:
                if event.text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    bet_amount += event.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    bet_amount = bet_amount[:-1]
        if open_chances == 0:
            screen.blit(egg_imgs_back[rarity_num], (0, 0))
            screen.blit(
                card_imgs[rarity_num],
                (
                    screen_width / 2 - card_imgs[rarity_num].get_width() / 2,
                    screen_height / 2 - card_imgs[rarity_num].get_height() / 2,
                ),
            )
            pygame.display.update()
            time.sleep(2)
            final_egg_rarity = rarity_num
            if final_egg_rarity < 5:
                eggs_since_good_reward += 1
            else:
                eggs_since_good_reward = 0
            income += INCOME_RARITY[final_egg_rarity]

            blobs.append(Blob(final_egg_rarity, blob_imgs))
            state = "Shop"
            open_chances = 6
            rarity_num = 0

        # draw
        screen.fill(WHITE)
        if state == "Job":
            if draw_job(
                earn_button,
                blobs,
                boost_button,
                boost_price,
                screen_width,
                screen_height,
            ):  # run job draw and check if income boost button pressed
                money -= boost_price

                # increase price of income boost
                if boost_price < 101:
                    boost_price *= 4
                elif boost_price < 5000:
                    boost_price *= 3
                else:
                    boost_price *= 2

                boost_price = round(boost_price)
        if state == "Casino":
            betting_numbers = draw_casino(
                bet_button,
                numbers,
                betting,
                bet_amount,
                win_loss_text,
                screen_width,
                screen_height,
            )
            betting = betting_numbers[0]
            numbers = betting_numbers[1]
        if state == "Shop":
            buying_egg = draw_shop(
                buy_egg_button, egg_price, money, screen_width, screen_height
            )
        if state == "Egg Open":
            draw_egg_opening(rarity_num, open_chances)
            buying_egg = False
        if betting:
            bet_timer += 0.010
        if bet_timer > 1:
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

                if bet_amount == "":
                    bet_amount = "0"
                money -= int(bet_amount)
                win_loss_text = "Oopsies. Try again. Sorry!"

        if buying_egg:
            state = "Egg Open"
            money -= egg_price

            if egg_price < 10000:
                egg_price *= 8
            elif egg_price < 10000000:
                egg_price *= 4
            elif egg_price < 100000000:
                egg_price = round(egg_price * 1.2)
            else:
                egg_price = egg_price

        if not state == "Egg Open":
            # draw tpo bar
            state = draw_text_bar(TITLE_TEXT, 55, state, screen)

        # update
        pygame.display.update()
        clock.tick(FPS)


# run game

if __name__ == "__main__":
    main()
