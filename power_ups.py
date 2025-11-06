import pygame
from pygame.sprite import Sprite
from random import randint

power_up_types = [
    {
        'name': 'ever_bullet',
        'img': 'images/laserGreenShot.bmp'
    },
    {
        'name': 'shield',
        'img': 'images/shield.bmp'
    },
    {
        'name': 'laser',
        'img': 'images/laserRed.bmp'
    },
]

class Powerups(Sprite):
    def __init__(self, game, type=power_up_types[0]):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.types = [
            {
                'name': 'ever_bullet',
                'img': 'images/laserGreenShot.bmp'
            },
            {
                'name': 'shield',
                'img': 'images/shield.bmp'
            },
            {
                'name': 'laser',
                'img': 'images/laserRed.bmp'
            },
        ]
        self.type = type['name']
        img = pygame.image.load(type['img'])
        self.image = pygame.transform.scale(img, (56,56))
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
        self.screen.blit(self.image, self.rect)
