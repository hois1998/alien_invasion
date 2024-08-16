import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        
        self.color = (60,60,60)
        self.speed = 5.0
        self.width = 30
        self.height = 10
        
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midright = ai_game.ship.rect.midright
        
        self.x = float(self.rect.x)
        
    def update(self):
        self.x += self.speed
        
        self.rect.x += int(self.x)
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
        