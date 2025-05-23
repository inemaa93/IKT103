import pygame
class Coins:
    coin_amount = 0 # Initialize the coin amount

    def __init__(self, x, y): # Initialize the coin
        self.images_coin = [] # Create an empty list to store the coin images
        self.index = 0
        self.counter = 0

        for num in range (1, 6): # Load and scale the coin images
            img_coin = pygame.image.load(f'Coin_img/coin{num}.png')
            img_coin = pygame.transform.scale(img_coin, (30, 30)) # Scale the coin
            self.images_coin.append(img_coin) # Add the coin image to the list

        self.image = self.images_coin[self.index] # Set the initial coin image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.fps = 60
        self.clock = pygame.time.Clock() #
        self.current_frame = 0
        self.frames = self.images_coin
        self.visible = True

        #Kilde:
        # line 25-42: Platformer/Part_3-Walking_Animation/platformer_tut3.py at master · russs123/Platformer · GitHub.”
        # Available: https://github.com/russs123/Platformer/blob/master/Part_3-Walking_Animation/platformer_tut3.py. [Accessed: May 18, 2024]

    def update(self):
        if self.visible:
            self.counter += 1
            if self.counter >= self.fps // 5:
                self.counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

    def draw(self, screen): # Draw the coin
        if self.visible: # Check if the coin is visible
            screen.blit(self.image, self.rect.topleft) # Draw the coin


    def coin_collision(self, other_rect):
        if self.visible and self.rect.colliderect(other_rect): # Check if the coin is visible and collides with the player
            self.visible = False # Set the coin to invisible
            Coins.coin_amount += 1 # Increase the coin amount
            return True
        return False