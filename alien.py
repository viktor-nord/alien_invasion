import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game, x=None, y=None):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('images/enemyShip.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = x if x!= None else self.rect.width
        self.rect.y = y if y!= None else self.rect.height
        self.x = float(self.rect.x)
        self.type = 'alien'
    
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_dir
        self.rect.x = self.x
    
    def check_edges(self):
        return (self.rect.right >= self.screen.get_rect().right) or (self.rect.left <= 0)

    def generate_fleet_grid(self):
        grid = []
        alien_width, alien_height = self.rect.size
        fleet_width, fleet_height = alien_width, alien_height
        while fleet_height < (self.settings.screen_height - 3 * alien_height):
            while fleet_width < (self.settings.screen_width - 2 * alien_width):
                grid.append({'x':fleet_width, 'y':fleet_height})
                fleet_width += 2 * alien_width
            fleet_width = alien_width
            fleet_height +=2 * alien_height
        return grid


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
