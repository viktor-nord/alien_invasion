In  Alien Invasion, the player controls a rocket ship that appears 
at the bottom center of the screen. The player can move the ship 
right and left using the arrow keys and shoot bullets using the 
spacebar. When the game begins, a fleet of aliens fills the sky 
and moves across and down the screen. The player shoots and 
destroys the aliens. If the player destroys all the aliens, a new fleet 
appears that moves faster than the previous fleet. If any alien hits 
the player’s ship or reaches the bottom of the screen, the player 
loses a ship. If the player loses three ships, the game ends.

multiple buttons

in alien_invasion.py

def __init__(self):
...
    self.play_button = Button(self, "Play")
    self.play_button_level_2 = Button(self, "Play Level 2", 1)
    self.play_button_level_3 = Button(self, "Play Level 3", 2)
...

def _update_screen(self):
...
    if not self.game_active:
        self.play_button.draw_button()
        self.play_button_level_2.draw_button()
        self.play_button_level_3.draw_button()

def _check_play_button(self, mouse_pos):
    level_1 = self.play_button.rect.collidepoint(mouse_pos)
    level_2 = self.play_button_level_2.rect.collidepoint(mouse_pos)
    level_3 = self.play_button_level_3.rect.collidepoint(mouse_pos)
    lv = 1
    if level_2:
        lv = 2
    elif level_3:
        lv = 3 
    button_clicked = level_1 or level_2 or level_3
    if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
        self.stats.level = lv
        self.settings.initialize_dynamic_settings(lv)

alien_invasion
12.1
12.2
13.1
13.2
14.1
14.4
14.5
14.6
14.7
12.3

games keys
12.5

games rocket
12.4
13.3
13.4

vertical
12.6
13.5
13.6
14.2
14.3
14.8