import pygame
import colorsys



class  Victoryflag:
    pygame.mixer.init()
    level_passed = pygame.mixer.Sound('music_sound/level-passed.mp3')
    def __init__(self, x, y): # Initialize the flag
        self.images_flag = []
        self.index = 0
        self.counter = 0

        for num in range (1, 6): # Load and scale the flag images
            img_flag = pygame.image.load(f'Flag/flag_{num}.png')
            img_flag = pygame.transform.scale(img_flag, (200, 200))
            self.images_flag.append(img_flag)

        self.image = self.images_flag[self.index] # Set the initial flag image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.current_frame = 0
        self.frames = self.images_flag

        # Kilde:
        # Line 25-42: Platformer/Part_3-Walking_Animation/platformer_tut3.py at master · russs123/Platformer · GitHub.”
        # Available: https://github.com/russs123/Platformer/blob/master/Part_3-Walking_Animation/platformer_tut3.py. [Accessed: May 18, 2024]

    def update(self): # Update the flag
        self.counter += 1
        if self.counter >= self.fps // 5:
            self.counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self, screen): # Draw the flag
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, other_rect): # Check if the flag collides with the player
        return self.rect.colliderect(other_rect)

    def rainbow_colors(self, step, total_steps): # Create a rainbow effect
        hue = step / total_steps
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return int(r * 255), int(g * 255), int(b * 255)

    def victory_flag_effect(self, coin_amount):
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(self.level_passed)
        screen = pygame.display.set_mode((1500, 640))
        black = (0, 0, 0)
        font = pygame.font.Font(None, 74)
        total_steps = 100  # Number of colors in the rainbow sequence
        duration = 3000  # Duration to display the effect in milliseconds
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < duration:
            for step in range(total_steps):
                screen.fill(black)
                text = font.render("Level Completed!", True, self.rainbow_colors(step, total_steps))
                text_rect = text.get_rect(center=(1500 // 2, 640 // 2))
                screen.blit(text, text_rect)
                text2 = font.render(f"Coins Collected: {coin_amount}", True, self.rainbow_colors(step, total_steps))
                text2_rect = text2.get_rect(center=(1500 // 2, 640 // 2 + 100))
                screen.blit(text2, text2_rect)
                pygame.display.flip()
                pygame.time.delay(10)  # Delay to create the animation effect
        pygame.time.wait(1000)  # Wait for 1 second after the animation