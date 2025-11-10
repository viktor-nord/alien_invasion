from pygame.sprite import Sprite
import pygame

frame_list = {
    'idle': {
        'img': 'images/demon/IDLE.bmp',
        'length': 4
    },
    'fly': {
        'img': 'images/demon/FLYING.bmp',
        'length': 4
    },
    'hurt': {
        'img': 'images/demon/HURT.bmp',
        'length': 4
    },
    'death': {
        'img': 'images/demon/DEATH.bmp',
        'length': 7
    }
}

class Boss(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        sprite_size = (64, 64)
        self.sprite_width = 80
        self.sprite_height = 70
        self.x = 10
        self.y = 10
        self.image = self.get_image(frame_list['idle']['img'], 0, 80, 70)
        self.rect = self.image.get_rect()
        self.timer = 0
        self.max_hp = 10
        self.hp = self.max_hp
        self.boss_status = 'none'

    def show_boss(self, action):
        new_action = action
        spacing = 10
        frame = 6 if self.boss_status == 'done' else 0
        if self.timer <= 1 * spacing:
            frame = 0
        elif self.timer <= 2 * spacing:
            frame = 1
        elif self.timer <= 3 * spacing:
            frame = 2
        elif self.timer <= 4 * spacing:
            frame = 3
        elif frame_list[new_action]['length'] == 7:
            if self.timer <= 5 * spacing:
                frame = 4
            elif self.timer <= 6 * spacing:
                frame = 5
            elif self.timer <= 7 * spacing:
                frame = 6
                self.boss_status = 'done'
        else:
            self.timer = 0
            new_action = 'idle'
        self.timer += 1
        image_path = frame_list[new_action]['img']
        if self.boss_status == 'active':
            self.image = self.get_image(image_path, frame, 80, 70)
        self.screen.blit(self.image, (self.x,self.y))
        return new_action

    def get_image(self, image_path, frame, width, height):
        img = pygame.Surface((width, height))
        sheet = pygame.image.load(image_path)
        img.blit(
            pygame.transform.flip(sheet, True, False), 
            (0,0), 
            (int(frame * width), 0, width, height)
        )
        img = pygame.transform.scale(img, (width * 3, height * 3))
        img.set_colorkey((0,0,0))
        return img
