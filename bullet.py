import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, 
                                self.settings.bullet_width, 
                                self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.type = 'regular'
    
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    
    def draw_bullet(self, type):
        if type == 'regular':
            pygame.draw.rect(self.screen, self.color, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

class EverBullet(Bullet):
    def __init__(self, game):
        super().__init__(game)
        self.type = 'ever'
        self.image = pygame.image.load('images/laserGreen.bmp')

class LaserBullet(Bullet):
    def __init__(self, game):
        super().__init__(game)
        self.type = 'laser'
        self.image = pygame.image.load('images/laserRed.bmp')
