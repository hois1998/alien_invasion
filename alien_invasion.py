import sys
import pygame
from random import randint
from time import sleep

import button
from settings import Settings
from ship import Ship
from brachio import Brachio
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviors.
    It works as control tower class among other classes because it takes other 
    classes into its consturctor to use and to provide some classes to other.
    """
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")
        
        # create an instance to store game statistics
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.brachio = Brachio(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self._create_fleet()
        # self._create_star_fleet()
        self.play_button = Button(self, 'Play')
        self.scoreboard = Scoreboard(self)
        
        self.fullscreen_mode = False
        
        # start alien invasion in an active state 
        self.game_active = False
    
    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
                
    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _create_star_fleet(self):
        max_cnt = 10
        
        star = Star(self)
        star_width, star_height = star.rect.size
        current_x, current_y = star_width, star_height
        
        cnt = 0
        while cnt < max_cnt:
            current_x = randint(0, 5)*star_width
            current_y = randint(0, 5)*star_height
            if current_y < (self.settings.screen_height - star_height):
                if current_x < (self.settings.screen_width - star_width):
                    new_star = Star(self)
                    new_star.rect.x = current_x
                    new_star.rect.y = current_y
                    self.stars.add(new_star)
                    cnt += 1
            
    def _create_fleet(self):
        # create an alien and keep adding aliens until there's no room left
        # spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        shift_row = False
        
        while current_y < (self.settings.screen_height-5*alien_height):
            while current_x < (self.settings.screen_width-2*alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            
            shift_row = not shift_row
            current_x = alien_width*1.5 if shift_row else alien_width
            current_y += 2*alien_height

    def _create_alien(self, x_position, y_position):
        """create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x, new_alien.rect.y = x_position, y_position
        self.aliens.add(new_alien)
        
    def run_game(self):
        while True:
            # handling events
            self._check_events()
            
            if self.game_active:
                # applying changes to game objects
                self.ship.update()
                # self.brachio.update()
                self._update_bullets()
                self._update_aliens()
            
            # render updated screen
            self._upadte_screen()
            # while is about 500fps to lower its value tick works as sleep waiti
            # until it satisfy 60 fps
            self.clock.tick(60) 
    
    def _update_aliens(self): 
        self._check_fleet_edges()
        self.aliens.update()
        
        # look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
        
    def _check_aliens_bottom(self):
        """check if any alien has reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
                
    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        # decrement ships left
        self.stats.ships_left -= 1
        
        if self.stats.ships_left > 0:
            # get rid of any remanining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            
            # create new fleet of alien and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
                    
    def _update_bullets(self):
        self.bullets.update()
        
        # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))     
        
        self._check_bullet_alien_collision()
    
    def _check_bullet_alien_collision(self):
        # check for any bullets that have hit aliens
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collision:
            self.stats.score += self.settings.alien_points*len(collision)
            self.scoreboard.prep_score()
        # check the fleet has been destroyed right after collosion with bullet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        
    def _check_events(self):
        """Response to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset the game settings
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.game_active = True
            # hide the mouse cursor
            pygame.mouse.set_visible(False)
            
    def _update_character_objects(self):
        self.ship = Ship(self)
        self.brachio = Brachio(self)
           
    def _check_key_f_events(self):
        if not self.fullscreen_mode:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self._update_character_objects()
            self.fullscreen_mode = True
        else:
            # 문제가 있다. 
            # 비록 settings의 클래스 값을 업데이트 하지만 여전히 업데이트가 안되는 것이 존재한다.
            self.settings.screen_width = Settings.default_screen_width
            self.settings.screen_height = Settings.default_screen_height
            self.screen = pygame.display.set_mode((
                self.settings.screen_width, self.settings.screen_height
            ))
            self._update_character_objects()
            self.fullscreen_mode = False
        
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            self.brachio.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            self.brachio.moving_left = True
        elif event.key == pygame.K_UP:
            self.brachio.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.brachio.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_f:
            self._check_key_f_events()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
            
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.brachio.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.brachio.moving_left = False
        elif event.key == pygame.K_UP:
            self.brachio.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.brachio.moving_down = False

    def _upadte_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        # self.brachio.blitme()
        self.aliens.draw(self.screen)
        # self.stars.draw(self.screen)
        
        self.scoreboard.show_score()
        # draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        
        # actually draw the screen with updated self.screen
        pygame.display.flip()
          
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()