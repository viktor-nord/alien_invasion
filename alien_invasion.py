import sys
import pygame
from random import randint, choice
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.game_active = False
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
        self.star_pattern = self._generate_star_pattern()
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.clock.tick(60)
            self._update_screen()

    #Helper Methods
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._add_stars()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(
            self.ship, self.aliens
        ) or self._check_aliens_bottom():
            self._ship_hit()

    def _check_aliens_bottom(self):
        is_game_over = False
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                is_game_over = True
        return is_game_over

    def _ship_hit(self):
        if self.stats.lives > 0:
            sleep(0.5)
            self.stats.lives -= 1
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_dir()
                break

    def _change_fleet_dir(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_dir *= -1

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Modified
            elif event.type == pygame.KEYDOWN:
                self._check_key_events(event.key, True)
            elif event.type == pygame.KEYUP:
                self._check_key_events(event.key, False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
                 
    # Modified
    def _check_key_events(self, key, is_key_down):
        if key == pygame.K_RIGHT:
            self.ship.moving_right = is_key_down
        elif key == pygame.K_LEFT:
            self.ship.moving_left = is_key_down
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE and is_key_down: 
            self._fire_bullet()
        elif key == pygame.K_p:
            cord = (self.play_button.rect.left + 1, self.play_button.rect.top + 1)
            # instead of creating a start game function
            self._check_play_button(cord)
    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, self.settings.is_not_super_bullet, True
        )
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _generate_star_pattern(self):
        pattern = []
        MARGIN = 100
        star_image = pygame.image.load('images/starBig.bmp')
        # star_image.get_rect() = (0, 0, 23, 21)
        x_count, y_count, width, height = star_image.get_rect()
        while y_count < self.settings.screen_height:
            while x_count < self.settings.screen_width:
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

    def _add_stars(self):
        for star in self.star_pattern:
            img = pygame.image.load(star['img'])
            self.screen.blit(img, (star['x'], star['y']))

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        fleet_width, fleet_height = alien_width, alien_height
        while fleet_height < (self.settings.screen_height - 3 * alien_height):
            while fleet_width < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(fleet_width, fleet_height)
                fleet_width += 2 * alien_width
            fleet_width = alien_width
            fleet_height +=2 * alien_height

    def _create_alien(self, x, y):
        new_alien = Alien(self)
        new_alien.x = x
        new_alien.rect.x = x
        new_alien.rect.y = y
        self.aliens.add(new_alien)
        



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()