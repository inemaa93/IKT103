# powerup.py
import pygame

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.image = pygame.image.load("player/powerup.png").convert_alpha()  # Add your power-up image here
        self.rect = pygame.Rect(self.x, self.y, self.width-16, self.height-16)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
