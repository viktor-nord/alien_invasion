import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        if self.settings.fullscreen:
            wh = (0, 0)
            f = pygame.FULLSCREEN
        else:
            wh = (self.settings.screen_width, self.settings.screen_height)
            f = 0
        self.screen = pygame.display.set_mode(wh, f)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    #Helper Methods
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Modified
            elif event.type == pygame.KEYDOWN:
                self._check_key_events(event.key, True)
            elif event.type == pygame.KEYUP:
                self._check_key_events(event.key, False)
                 
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        pygame.display.flip()

    # Modified
    def _check_key_events(self, key, is_key_down):
        if key == pygame.K_UP:
            self.ship.moving_up = is_key_down
        elif key == pygame.K_DOWN:
            self.ship.moving_down = is_key_down
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE and is_key_down: 
            self._fire_bullet()
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width:
                self.bullets.remove(bullet)


    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()