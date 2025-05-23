import pygame
import Sprit_loader


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.velocity = 30
        self.gravity = 1
        self.jump_height = 20
        self.vertical_velocity = 0
        self.ground_height = 336
        self.jumping = False
        self.running_right = False
        self.running_left = False
        self.on_ground = True
        self.jump_sound = pygame.mixer.Sound("music_sound/sound6.mp3")
        self.ouch_sound = pygame.mixer.Sound("music_sound/ouch.mp3")
        self.powerup_sound = pygame.mixer.Sound("music_sound/powerUp.wav")

        self.rect = pygame.Rect(self.x, self.y, self.width - 20, self.height - 6)

        self.load_images()

        self.animation_list_for_idle = []
        self.animation_steps_for_idle = 11

        self.animation_list_for_running_right = []
        self.animation_list_for_running_left = []
        self.animation_steps_for_running = 11

        self.last_animation_time = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame_counter_idle = 0
        self.frame_counter_running = 0

        self.load_animations()

    def load_images(self):
        self.player_object_idle = pygame.image.load("player/Idle.png").convert_alpha()
        self.player_object_jumping = pygame.image.load("player/Jump (32x32).png").convert_alpha()
        self.player_object_jumping = pygame.transform.scale(self.player_object_jumping, (self.width, self.height))
        self.player_object_running_right = pygame.image.load("player/Run (32x32).png").convert_alpha()
        self.player_object_running_left = pygame.transform.flip(self.player_object_running_right, True, False)

        self.sprite_idle_animation = Sprit_loader.SpritLoader(self.player_object_idle)
        self.sprite_running_animation_right = Sprit_loader.SpritLoader(self.player_object_running_right)
        self.sprite_running_animation_left = Sprit_loader.SpritLoader(self.player_object_running_left)

    #Kilde: “pygame_tutorials/sprite_tutorial at main · russs123/pygame_tutorials,” GitHub.
    # Available: https://github.com/russs123/pygame_tutorials/tree/main/sprite_tutorial. [Accessed: May 24, 2024]

    def load_animations(self):
        self.animation_list_for_idle = []
        self.animation_list_for_running_right = []
        self.animation_list_for_running_left = []

        for i in range(self.animation_steps_for_idle):
            image = self.sprite_idle_animation.get_image(i, 32, 32, 2, "black")
            scaled_image = pygame.transform.scale(image, (self.width, self.height)).convert_alpha()
            self.animation_list_for_idle.append(scaled_image)

        for i in range(self.animation_steps_for_running):
            image_right = self.sprite_running_animation_right.get_image(i, 32, 32, 2, "black")
            scaled_image_right = pygame.transform.scale(image_right, (self.width, self.height)).convert_alpha()
            self.animation_list_for_running_right.append(scaled_image_right)

            image_left = self.sprite_running_animation_left.get_image(i, 32, 32, 2, "black")
            scaled_image_left = pygame.transform.scale(image_left, (self.width, self.height)).convert_alpha()
            self.animation_list_for_running_left.append(scaled_image_left)

    #Kilde:
    # “pygame_tutorials/sprite_tutorial at main · russs123/pygame_tutorials,” GitHub.
    # Available: https://github.com/russs123/pygame_tutorials/tree/main/sprite_tutorial. [Accessed: May 24, 2024]

    def handle_input(self, dt):
        pygame.joystick.init()
        controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for controller in controllers:
            controller.init()

        keys = pygame.key.get_pressed()
        hat_x = 0
        hat_y = 0
        axis_x = 0
        axis_y = 0

        if controllers:
            for controller in controllers:
                if controller.get_numhats() > 0:
                    hat_x, hat_y = controller.get_hat(0)
                if controller.get_numaxes() > 0:
                    axis_x = controller.get_axis(0)
                    axis_y = controller.get_axis(1)

        if keys[pygame.K_RIGHT] or hat_x == 1 or axis_x > 0.1:
            self.x += self.velocity * dt
            self.running_right = True
        else:
            self.running_right = False

        if keys[pygame.K_LEFT] or hat_x == -1 or axis_x < -0.1:
            self.x -= self.velocity * dt
            self.running_left = True
        else:
            self.running_left = False

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE] or hat_y == 1 or (controllers and controller.get_button(0))
            or axis_y < -0.5) and not self.jumping:
            self.jumping = True
            self.on_ground = False
            pygame.mixer.Sound.play(self.jump_sound)
            self.vertical_velocity = -self.jump_height

    #Kilde til controller inputs:
    # “pygame.joystick — pygame v2.6.0 documentation.”
    # Available: https://www.pygame.org/docs/ref/joystick.html. [Accessed: May 18, 2024]

    def update(self, dt):
        if self.jumping:
            self.y += self.vertical_velocity
            self.vertical_velocity += self.gravity
            if self.y >= self.ground_height:
                self.y = self.ground_height
                self.jumping = False
                self.on_ground = True
        else:
            if not self.on_ground:
                self.vertical_velocity += self.gravity
                self.y += self.vertical_velocity
                if self.y >= self.ground_height:
                    self.y = self.ground_height
                    self.on_ground = True
                    self.vertical_velocity = 0

        self.rect.topleft = (self.x, self.y)
        self.update_animation()

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.running_right:
            if current_time - self.last_animation_time >= self.animation_cooldown:
                self.frame_counter_running += 1
                self.last_animation_time = current_time
                if self.frame_counter_running >= len(self.animation_list_for_running_right):
                    self.frame_counter_running = 0
        elif self.running_left:
            if current_time - self.last_animation_time >= self.animation_cooldown:
                self.frame_counter_running += 1
                self.last_animation_time = current_time
                if self.frame_counter_running >= len(self.animation_list_for_running_left):
                    self.frame_counter_running = 0
        else:
            if current_time - self.last_animation_time >= self.animation_cooldown:
                self.frame_counter_idle += 1
                self.last_animation_time = current_time
                if self.frame_counter_idle >= len(self.animation_list_for_idle):
                    self.frame_counter_idle = 0

    # Kilde:
    # “pygame_tutorials/sprite_tutorial at main · russs123/pygame_tutorials,” GitHub.
    # Available: https://github.com/russs123/pygame_tutorials/tree/main/sprite_tutorial. [Accessed: May 16, 2024]

    def draw(self, screen):
        if self.jumping and not self.on_ground:
            screen.blit(self.player_object_jumping, (self.x, self.y))
        elif self.running_right:
            screen.blit(self.animation_list_for_running_right[self.frame_counter_running], (self.x, self.y))
        elif self.running_left:
            screen.blit(self.animation_list_for_running_left[self.frame_counter_running], (self.x, self.y))
        else:
            screen.blit(self.animation_list_for_idle[self.frame_counter_idle], (self.x, self.y))

    def handle_collision(self, boxes):
        self.on_ground = True  # Assume player is not on the ground
        box_to_remove = None
        for box in boxes:
            if self.rect.colliderect(box.rect):
                if self.rect.bottom <= box.rect.top + self.vertical_velocity:
                    self.rect.bottom = box.rect.top
                    self.y = self.rect.top
                    self.vertical_velocity = 0
                    self.jumping = False
                    self.on_ground = True
                elif self.rect.top >= box.rect.bottom + self.vertical_velocity and self.vertical_velocity < 0:
                    self.rect.top = box.rect.bottom
                    self.y = self.rect.top
                    self.vertical_velocity = 0
                    pygame.mixer.Sound.play(self.ouch_sound)
                    box_to_remove = box
                elif self.rect.right > box.rect.left and self.rect.left < box.rect.left:
                    self.rect.right = box.rect.left
                    self.x = self.rect.left

                elif self.rect.left < box.rect.right and self.rect.right > box.rect.right:
                    self.rect.left = box.rect.right
                    self.x = self.rect.left
        if box_to_remove:
            boxes.remove(box_to_remove)

        # If the player is not colliding with any box and is above the ground level, set on_ground to False
        if self.y < self.ground_height and not any(self.rect.colliderect(box) for box in boxes):
            self.on_ground = False

    def handle_collision_with_powerup(self, powerups):
        for powerup in powerups:
            if self.rect.colliderect(powerup.rect):
                self.increase_size()
                powerups.remove(powerup)

    def increase_size(self):
        self.width += 20  # Increase width
        self.height += 20  # Increase height
        self.ground_height -= 20
        pygame.mixer.Sound.play(self.powerup_sound)

        self.rect = pygame.Rect(self.x, self.y, self.width - 20, self.height - 6)
        self.player_object_jumping = pygame.transform.scale(self.player_object_jumping,
                                                            (self.width, self.height)).convert_alpha()
        self.load_animations()  # Reload animations with new size
