import pygame
from pygame.sprite import Sprite

from power_ups import Powerups, power_up_types

class Ship(Sprite):
    def __init__(self, game, small=False):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load(
            'images/life.bmp'
        ) if small else pygame.image.load('images/player.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 10
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.number_of_ever_bullets = 0
        self.number_of_shields = 0
        self.shield = Powerups(game, power_up_types[1])
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        if self.number_of_shields > 0:
            self.shield.rect.center = self.rect.center
            self.screen.blit(self.shield.image, self.shield.rect)
    
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