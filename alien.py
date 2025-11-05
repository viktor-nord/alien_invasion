import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('images/enemyShip.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = 'alien'
    
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_dir
        self.rect.x = self.x
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

class Ufo(Alien):
    def __init__(self, game):
        super().__init__(game)
        self.image = pygame.image.load('images/enemyUFO.bmp')
        self.type = 'ufo'
        self.direction = 1
        self.gravity = 1
        self.bounce_height = 20
        self.velocity = self.bounce_height

    def update(self):
        self.x += self.settings.alien_speed * self.direction
        self.rect.x = self.x
        self.rect.y += self.velocity
        self.velocity -= self.gravity
        if self.velocity < self.bounce_height * -1:
            self.velocity = self.bounce_height
