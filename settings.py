class Settings:
    """A class to store all setttings for Alien Invasion"""
    # default settings 
    default_screen_width = 1200
    default_screen_height = 800
    default_bg_color = (230, 230, 230)
    
    def __init__(self):
        """initialize the game's static settings"""
        # screen settings 
        self.screen_width = Settings.default_screen_width
        self.screen_height = Settings.default_screen_height
        self.bg_color = Settings.default_bg_color
                
        # ship settings
        self.ship_speed: float = 3.0
        self.brachio_speed: float = 5.0
        self.ship_limit = 3
        
        # bullet settings
        self.bullet_speed = 4
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.max_bullet_num = 10
        
        # Alien settings
        self.alien_speed = 10.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 represents right, -1 represents left
        
        # how quickly the game speeds up
        self.speedup_scale = 1.1
        
        # how quickly the alien point values increase
        self.alien_points_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.alien_speed = 3.0
        self.bullet_speed = 3.0
        
        # fleet direction
        # represents 1 as right and -1 as left
        self.fleet_direction = 1
        
        # score settings
        self.alien_points = 50
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        
        