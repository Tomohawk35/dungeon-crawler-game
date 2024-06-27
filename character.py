import pygame
import constants
import math

class Character:
    def __init__(self, x: int, y: int, health, mob_animations: list[list[pygame.Surface]], char_type, boss: bool, size) -> None:
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0 # 0: Idle, 1: Run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)

    def move(self, dx: int, dy: int, obstacle_tiles) -> None:
        screen_scroll = [0, 0]
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

        # Check for collision with map in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            # Check for collisions
            if obstacle[1].colliderect(self.rect):
                # Check which side the collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            # Check for collisions
            if obstacle[1].colliderect(self.rect):
                # Check which side the collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        # Logic only applicable to player
        if self.char_type == 0:

            # Update scroll based on player position
            # Move camera left and right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
            if self.rect.left < (constants.SCROLL_THRESH):
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH
            # Move camera up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
            if self.rect.top < (constants.SCROLL_THRESH):
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH
        
        return screen_scroll

    def ai(self, screen_scroll):
        
        # Reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def update(self):
        # Check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
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
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, constants.RED, self.rect, 1)