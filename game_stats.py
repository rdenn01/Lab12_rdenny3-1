"""
Settings
Ryan Denny

This represents stat handling for the next unit which I accidentally started working on.
Thus, it is not used.

7/27/2020
"""

class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit