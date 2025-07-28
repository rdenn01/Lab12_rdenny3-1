"""
Alien Invasion Game
Ryan Denny

This program includes game logic for a game where you control a spaceship, 
moving it up and down and pressing space to shoot.

7/27/2025
"""

import sys
import pygame
import time

from settings import Settings
from bullet import Bullet
from game_stats import GameStats
from alien import Alien
from button import Button

class Ship:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image = pygame.image.load('Assets/images/ship.png')
        self.rect = self.image.get_rect()

        self.rect.midright = self.screen_rect.midright

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up and self.rect.top > 0:
             self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < game.settings.screen_height - 15:
             self.y += self.settings.ship_speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def blitme(self):
        rotated_image = pygame.transform.rotate(self.image, 90)
        self.screen.blit(rotated_image, self.rect)

    def center_ship(self):
        self.rect.midright = self.screen_rect.midright
        self.y = float(self.rect.y)
        

class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()
        self.game_active = True

        self.play_button = Button(self, "Play")

    def game_loop(self):
        while True:
            self.check_events()

            if self.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
            self.clock.tick(60)
    
    def update_screen(self):
            self.screen.fill(self.settings.bg_color)

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.ship.blitme()
            self.aliens.draw(self.screen)

            if not self.game_active:
                self.play_button.draw_button

            pygame.display.flip()

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left < 0:
                print("removing bullet")
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        self.check_alien_bottom()

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self.check_keyup_events(event)
                    

    def check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
             sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_alien_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.settings.screen_width:
                self.ship_hit()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.x += self.settings.drop_speed
        self.settings.fleet_direction *= -1

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            self.create_fleet()
            self.ship.center_ship()

            time.sleep(0.5)
        else:
            self.game_active = False
    
    def create_fleet(self):
        alien = Alien(self)
        self.aliens.add(alien)

        alien_width, alien_height = alien.rect.width, alien.rect.height
        current_x, current_y = alien_width, alien_height

        col_limit = 8
        curr_col = 0

        while current_x < (self.settings.screen_width - 3 * alien_width) and curr_col < col_limit:
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self.create_alien(current_x, current_y)
                current_y += 2 * alien_height
            current_y = alien_height
            current_x += 2 * alien_width
            curr_col += 1
    
    def create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


if __name__ == '__main__':
    game = AlienInvasion()
    game.game_loop()