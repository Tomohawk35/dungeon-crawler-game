import pygame
import constants
import math

class Character:
    def __init__(self, x: int, y: int, animation_list: list[list[pygame.Surface]]) -> None:
        self.flip = False
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 # 0: Idle, 1: Run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.image = animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)

    def move(self, dx: int, dy: int) -> None:
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
            
        # Control facing direction
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        # Control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # Check what action the player is performing
        if self.running == True:
            self.update_action(1) # 1: Run
        else: 
            self.update_action(0) # 0: Idle
        animation_cooldown = 70
        # Handle animation
        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, surface: pygame.Surface) -> None:
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)