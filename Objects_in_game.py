import pygame

class My_GameObject:

    def __init__(self, x, y, width, height, image_used):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_used = image_used

        image = pygame.image.load(image_used)
        self.image = pygame.transform.scale(image, (self.width, self.height))
