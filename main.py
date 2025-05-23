# main.py
import pygame
import sys
import player
import Objects_in_game
import colorsys
from Victory import Victoryflag
from coin import Coins
from powerup import PowerUp

pygame.init()

def render_coin_amount(screen): # Render the coin amount
    coin_text = font.render(f'Coins: {Coins.coin_amount}', True, (255, 255, 255))  # White color
    screen.blit(coin_text, (10, 10))

# loading the background
layers_background = [ pygame.image.load("Background layers/Night.png"),
                      pygame.image.load("Background layers/Far Forest.png"),
                      pygame.image.load("Background layers/Dark Tree.png"),
    ]
# Scale the background layers to match the screen size
layers_background = [pygame.transform.scale(layer, (1500, 640)) for layer in layers_background]

background_color = (50, 50, 50)
font = pygame.font.Font(None, 36)
black = (0, 0, 0)

clock = pygame.time.Clock()
music = pygame.mixer.music.load("music_sound/Clement Panchout _ 80s Zombies Movie _ 2018.wav")
coin_pickup = pygame.mixer.Sound('music_sound/pickupCoin.wav')
level_passed = pygame.mixer.Sound('music_sound/level-passed.mp3')
pygame.mixer.music.play(-1)

# Detect controllers
pygame.joystick.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for controller in controllers:
    controller.init()
# Kilde:
# “pygame.joystick — pygame v2.6.0 documentation.”
# Available: https://www.pygame.org/docs/ref/joystick.html. [Accessed: May 18, 2024]

screen = pygame.display.set_mode((1500, 640))
pygame.display.set_caption("Python Mario game like assignment *Jump Man*")

# Initialize player
player = player.Player(0, 336)

# Initialize victory flag
victory_flag = Victoryflag(1450, 320)

# Adding in coins
coins = [
    Coins(232, 322),
    Coins(532, 322),
    Coins(832, 322),
    Coins(632, 40),
    Coins(982, 40)
]

# Adding in boxes
boxes = [
    Objects_in_game.My_GameObject(200, 344, 64, 64, "Boxes/idle.png"),
    Objects_in_game.My_GameObject(500, 344, 64, 64, "Boxes/idle.png"),
    Objects_in_game.My_GameObject(800, 344, 64, 64, "Boxes/idle.png"),
    Objects_in_game.My_GameObject(600, 144, 64, 64, "Boxes/idle.png"),
    Objects_in_game.My_GameObject(950, 144, 64, 64, "Boxes/idle.png"),
]

# Adding in power-ups
powerups = [
    PowerUp(622, 163),
    PowerUp(960, 163)

]

# Gives each box has a rect for collision and breaking the floating block
for box in boxes:
    box.rect = pygame.Rect(box.x, box.y, 64-20, 64-15)

while True:
    screen.fill((255, 255, 255))
    dt = clock.tick(60) / 100

    for layer in layers_background:
        screen.blit(layer, (0, -240))

    pygame.draw.rect(screen, " darkgreen", (0, 400, 2000, 300))
    pygame.draw.rect(screen, "gray", (0, 400, 2000, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.handle_input(dt)
    player.update(dt)
    player.handle_collision(boxes)
    player.handle_collision_with_powerup(powerups)

    player.draw(screen)
    for powerup in powerups:
        powerup.draw(screen)
    for box in boxes:
        screen.blit(box.image, (box.x, box.y))

    victory_flag.update()
    victory_flag.draw(screen)

    # Update coin and handle collision
    for coin in coins:
        if coin.coin_collision(player):  # Assuming player has a rect attribute
            coin_pickup.play()
        coin.update()  # Update the coin animation

    # Draw coins
    for coin in coins:
        coin.draw(screen)

    if victory_flag.check_collision(player):
        coin_amount = Coins.coin_amount
        victory_flag.victory_flag_effect(coin_amount)

    render_coin_amount(screen)

    pygame.display.flip()
