import pygame
from random import randint, choice

class Settings:
    def __init__(self):
        # Screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (171, 70, 203)
        self.fullscreen = False
        # Ship and power ups
        self.lives = 3
        # Bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.ever_bullet_color = (0, 191, 255)
        self.bullets_allowed = 3
        # Alien
        self.fleet_drop_speed = 15
        self.alien_points = 50
        # Player
        self.ever_bullet = False
        self.shied = False
        self.laser = False
        # Level
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 5
        self.bullet_speed = 10
        self.alien_speed = 3
        self.fleet_dir = 1 #1=right -1=left

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
    
    def get_screen(self):
        wh = (0, 0) if self.fullscreen else (self.screen_width, self.screen_height)
        f = pygame.FULLSCREEN if self.fullscreen else 0
        return pygame.display.set_mode(wh, f)

    def generate_star_pattern(self):
        pattern = []
        MARGIN = 100
        star_image = pygame.image.load('images/starBig.bmp')
        x_count, y_count, width, height = star_image.get_rect()
        while y_count < self.screen_height:
            while x_count < self.screen_width:
                star = {
                    'img': choice(
                        ['images/starBig.bmp', 'images/starSmall.bmp']
                    ), 
                    'x': randint(x_count, x_count + MARGIN - width),
                    'y': randint(y_count, y_count + MARGIN - height)
                }
                pattern.append(star)
                x_count += MARGIN
            y_count += MARGIN
            x_count = 0
        return pattern