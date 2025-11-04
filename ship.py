import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game, small=False):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        if small:
            self.image = pygame.image.load('images/life.bmp')
        else:
            self.image = pygame.image.load('images/player.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 10
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.number_of_ever_bullets = 0
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            self.image = pygame.image.load('images/playerRight.bmp')
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            self.image = pygame.image.load('images/playerLeft.bmp')
        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)