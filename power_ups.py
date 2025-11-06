import pygame
from pygame.sprite import Sprite
from random import randint

power_up_types = [
    {
        'name': 'ever_bullet',
        'img': 'images/laserGreen.bmp', # 56,54
        'falling_image': 'images/laserGreenShot.bmp',
        'scale': (56, 54)
    },
    {
        'name': 'shield',
        'img': 'images/shield.bmp', # 151,118
        'falling_image': 'images/shield.bmp',
        'scale': (76, 60)
    },
    {
        'name': 'laser',
        'img': 'images/laserRed.bmp', #9,30
        'falling_image': 'images/laserRedShot.bmp',
        'scale': (56, 54)
    },
]

class Powerups(Sprite):
    def __init__(self, game, type=power_up_types[0]):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.type = type['name']
        self.image = pygame.image.load(type['img'])
        img = pygame.image.load(type['falling_image'])
        self.falling_image = pygame.transform.scale(img, type['scale'])
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = randint(-1000, -100)
        self.fall_speed = 1
    
    def update(self):
        if self.rect.y > self.screen.get_rect().height:
           self.rect.y = randint(-1000, -100)
        else:
            self.rect.y += self.fall_speed

    def blitme(self):
        self.screen.blit(self.falling_image, self.rect)
