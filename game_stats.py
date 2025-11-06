from pathlib import Path
import json

class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.high_score = json.loads(
            (Path('high_score.json').read_text())
        )['high_score']
        self.reset_stats()

    def reset_stats(self):
        self.lives = self.settings.lives
        self.score = 0
        self.level = 1

    def get_caped_level_list(self):
        if self.level == 1:
            lv = 0
        elif self.level > 10:
            lv = 10
        else:
            lv = self.level - 1
        return list(range(lv))