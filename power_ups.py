import pygame
from pygame.sprite import Sprite
from random import randint

class Powerups(Sprite):
    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        types = ['ever_bullet', 'shied', 'laser',]
        self.type = types[type]
        self.image = pygame.image.load(f'images/laserGreenShot.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = randint(-3000, -100)
        self.fall_speed = 1
        self.number_of_uses = 0
    
    def update(self):
        if self.rect.y > self.screen.get_rect().height:
           self.rect.y = randint(-3000, -100)
        else:
            self.rect.y += self.fall_speed
