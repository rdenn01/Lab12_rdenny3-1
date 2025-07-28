"""
Settings
Ryan Denny

This stores settings such as screen settings and bullets.

7/27/2020
"""

class Settings:

    def __init__(self):
        # Screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Bullets
        self.bullet_speed = 15.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Aliens
        self.alien_speed = 3.0
        self.drop_speed = 10
        self.fleet_direction = 1
    
        # Ship
        self.ship_limit = 3
        self.ship_speed = 3