import numpy 
import pygame

from sideway_settings import Settings

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_heigth)
        )
        self.clock = pygame.time.Clock()
        
    def run_game(self):
        """start the main loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            
            # redraw the screen background
            self.screen.fill(self.settings.bg_color)
            # make the most drawn screen visible
            pygame.display.flip()
            self.clock.tick(self.settings.fps)
            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
            
            