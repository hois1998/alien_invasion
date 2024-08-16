import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # load the ship image and get its rect
        image = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.rotate(image, -90)
        self.rect = self.image.get_rect()
        
        # load the screen rect
        self.screen_rect = self.screen.get_rect()
        
        # set ship image rect at midleft of the screen
        self.rect.midleft = self.screen_rect.midleft
        
        # set ship to move
        self.move_down, self.move_up = False, False
        self.ship_direction = 1
        self.ship_speed = 2.0
        
    def update(self):
        if (self.move_down and self.rect.bottom < self.screen_rect.bottom and (self.ship_direction+1)) or \
           (self.move_up and self.rect.top > self.screen_rect.top and (self.ship_direction-1)):
            self.rect.y += int(self.ship_speed*self.ship_direction)
    
    def blitme(self):
        """change part: draw the ship at its current positon"""
        self.screen.blit(self.image, self.rect)
        
    
    
        