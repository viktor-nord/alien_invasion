class Settings:
    def __init__(self, level=1):
        # Screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (171, 70, 203)
        self.fullscreen = False
        # Ship
        self.lives = 3
        # Bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien
        self.fleet_drop_speed = 10
        self.alien_points = 50
        # Player
        self.is_not_super_bullet = True
        # Level
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings(level)

    def initialize_dynamic_settings(self, level=1):
        for num in range(1, level + 1):
            self.ship_speed = 1.5
            self.bullet_speed = 2.5
            self.alien_speed = 5
            self.fleet_dir = 1 #1=right -1=left

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)