import sys
import pygame
from time import sleep
from random import choice

from settings import Settings
from ship import Ship
from bullet import Bullet, EverBullet
from alien import Alien, Ufo
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from power_ups import Powerups, power_up_types

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.screen = self.settings.get_screen()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.star_pattern = self.settings.generate_star_pattern()
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.powerup = Powerups(self, choice(power_up_types))
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._generate_power_ups()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)
        
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_powerups()
                self._update_bullets()
                self._update_aliens()
                self.clock.tick(60)
            self._update_screen()

    # Create
    def _create_fleet(self):
        grid = Alien(self).generate_fleet_grid()
        for pos in grid:
            self._create_alien(pos['x'], pos['y'])
        for x in self.stats.get_caped_level_list():
            ufo = Ufo(self)
            ufo.x = 10 + x * (ufo.rect.width + 10)
            self.aliens.add(ufo)

    def _create_alien(self, x, y):
        new_alien = Alien(self, x, y)
        new_alien.x = x
        self.aliens.add(new_alien)

    def _generate_power_ups(self):
        type = choice(power_up_types)
        self.powerup = Powerups(self, type)

    def _draw_bullets(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet(bullet.type)

    def _draw_stars(self):
        for star in self.star_pattern:
            img = pygame.image.load(star['img'])
            self.screen.blit(img, (star['x'], star['y']))

    def _fire_bullet(self):
        if self.ship.number_of_ever_bullets > 0:
            self.ship.number_of_ever_bullets -=1
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            if self.ship.number_of_ever_bullets > 0:
                new_bullet = EverBullet(self)
            self.bullets.add(new_bullet)

    # Update
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._draw_stars()
        self._draw_bullets()
        self.aliens.draw(self.screen)
        self.powerup.blitme()
        self.ship.blitme()
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _update_powerups(self):
        if self.ship.rect.colliderect(self.powerup.rect):
            if self.powerup.type == 'ever_bullet':
                self.ship.number_of_ever_bullets = 5
            if self.powerup.type == 'shield':
                self.ship.number_of_shields = 1
            self._generate_power_ups()
        self.powerup.update()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        collide = pygame.sprite.spritecollideany(self.ship, self.aliens)        
        if collide and self.ship.number_of_shields > 0:
            self.aliens.remove(collide)
            self.ship.number_of_shields -= 1
            collide = None
        if self._check_aliens_bottom():
            self._ship_hit()

    # Check
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                if alien.type == 'alien':
                    self._change_fleet_dir()
                else:
                    alien.rect.y += self.settings.fleet_drop_speed
                    alien.direction *= -1
                break

    def _change_fleet_dir(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_dir *= -1

    def _check_aliens_bottom(self):
        is_game_over = False
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                is_game_over = True
        return is_game_over

    def _check_events(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            self.ship.moving_left = keys[pygame.K_LEFT]
            self.ship.moving_right = keys[pygame.K_RIGHT]
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif keys[pygame.K_p]:
                self._check_play_button(self.play_button.rect.center)
            elif event.type == pygame.KEYUP:
                self.ship.image = pygame.image.load('images/player.bmp')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, pos):
        if self.play_button.rect.collidepoint(pos) and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True
            self.reset_sprites()
            pygame.mouse.set_visible(False)

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, True
        )
        if collisions:
            for bullet, aliens in collisions.items():
                if bullet.type == 'regular':
                    self.bullets.remove(bullet)
                points = self.settings.alien_points
                for alien in aliens:
                    points += self.settings.screen_height - alien.rect.y
                self.stats.score += points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.settings.increase_speed()
            self.stats.level += 1
            self.reset_sprites()

    def _ship_hit(self):
        if self.stats.lives > 0:
            sleep(0.5)
            self.stats.lives -= 1
            self.reset_sprites()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def reset_sprites(self):
        self.sb.prep_images()
        self.bullets.empty()
        self.aliens.empty()
        self._generate_power_ups()
        self.ship.center_ship()
        self._create_fleet()
        self._generate_power_ups()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    pygame.quit()