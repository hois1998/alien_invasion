import pygame

class Ship:
    """A class to manage ship"""
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.screen_rect = ai_game.screen.get_rect()
        
        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        # start each new ship at the bottom center of the screen 
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
            
        self.rect.x = int(self.x)
    
    # def update_screen(self, settings):
    #     self.screen
    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)