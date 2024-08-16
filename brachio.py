import pygame

class Brachio:
    """manage brachio character"""
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.screen_rect = ai_game.screen.get_rect()
        
        self.image = pygame.image.load('images/brachio.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.center = self.screen_rect.center
        
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self):
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.brachio_speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.brachio_speed
            
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.brachio_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.brachio_speed
            
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        
    
        