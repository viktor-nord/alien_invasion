import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet, EverBullet
from alien import Alien, Ufo
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from power_ups import Powerups

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
        self.power_ups = pygame.sprite.Group()
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

    #Helper Methods
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self._draw_stars()
        self._draw_bullets()
        self.aliens.draw(self.screen)
        self.power_ups.draw(self.screen)
        self.ship.blitme()
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _draw_bullets(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet(bullet.type)

    def _draw_stars(self):
        for star in self.star_pattern:
            img = pygame.image.load(star['img'])
            self.screen.blit(img, (star['x'], star['y']))

    def _generate_power_ups(self):
        powerup = Powerups(self, 0)
        self.power_ups.add(powerup)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(
            self.ship, self.aliens
        ) or self._check_aliens_bottom():
            self._ship_hit()

    def _update_powerups(self):
        collide = pygame.sprite.spritecollideany(self.ship, self.power_ups)
        if collide:
            if collide.type == 'ever_bullet':
                self.ship.number_of_ever_bullets = 5
            self.power_ups.remove(collide)
            self._generate_power_ups()
        self.power_ups.update()

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
            self.sb.prep_ships()
            self.reset_sprites()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

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
            self.sb.prep_images()
            self.game_active = True
            self.reset_sprites()
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """pygame.sprite.groupcollide
        takes in 4 arguments. 
        1. a sprite groupe that might collide with something
        2. a sprite groupe that the first groupe sprite might collide into
        3. if the first sprite should diaper when colliding 
        4. if the second sprite should diaper when colliding

        this returns a dictionary where the first sprite groupe is the key 
        and the second sprite groupe is the value
        """
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
            self.sb.prep_level()
            self.reset_sprites()

    def reset_sprites(self):
        self.bullets.empty()
        self.aliens.empty()
        self.power_ups.empty()
        self.ship.center_ship()
        self._create_fleet()
        self._generate_power_ups()

    def _fire_bullet(self):
        if self.ship.number_of_ever_bullets > 0:
            self.ship.number_of_ever_bullets -=1
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            if self.ship.number_of_ever_bullets > 0:
                new_bullet = EverBullet(self)
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
        for x in self.stats.get_caped_level_list():
            ufo = Ufo(self)
            ufo.x = 10 + x * (ufo.rect.width + 10)
            self.aliens.add(ufo)

    def _create_alien(self, x, y):
        new_alien = Alien(self, x, y)
        new_alien.x = x
        self.aliens.add(new_alien)
        

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    pygame.quit()