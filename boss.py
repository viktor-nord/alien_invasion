from pygame.sprite import Sprite
import pygame

def get_image(sheet, frame, width, height):
    img = pygame.Surface((width, height))
    img.blit(sheet, (0,0), (int(frame * width), 0, width, height))
    img = pygame.transform.scale(img, (width * 3, height * 3))
    img.set_colorkey((0,0,0))
    return img

idle_image = pygame.image.load('images/demon/IDLE.bmp')
idle_0 = get_image(idle_image, 0, 79, 69)
idle_1 = get_image(idle_image, 1, 79, 69)
idle_2 = get_image(idle_image, 2, 79, 69)
idle_3 = get_image(idle_image, 3, 79, 69)
idle = [idle_0, idle_1, idle_2, idle_3]

fly_image = pygame.image.load('images/demon/FLYING.bmp')
fly_0 = get_image(fly_image, 0, 79, 69)
fly_1 = get_image(fly_image, 1, 79, 69)
fly_2 = get_image(fly_image, 2, 79, 69)
fly_3 = get_image(fly_image, 3, 79, 69)
fly = [fly_0, fly_1, fly_2, fly_3]

hurt_image = pygame.image.load('images/demon/HURT.bmp')
hurt_0 = get_image(hurt_image, 0, 79, 69)
hurt_1 = get_image(hurt_image, 1, 79, 69)
hurt_2 = get_image(hurt_image, 2, 79, 69)
hurt_3 = get_image(hurt_image, 3, 79, 69)
hurt = [hurt_0, hurt_1, hurt_2, hurt_3]

frame_list = {
    'idle': idle,
    'fly': fly,
    'hurt': hurt,
}

class Boss(Sprite):
    def __init__(self, game, action='idle'):
        super().__init__()
        self.screen = game.screen
        sprite_size = (64, 64)
        self.sprite_width = 79
        self.sprite_height = 69
        self.sprite_surface = pygame.Surface((64,64))
        self.timer = 0
        self.frames = frame_list[action]

    def show_boss(self, action):
        self.frames = frame_list[action]
        new_action = action
        if self.timer <= 10:
            frame = self.frames[0]
        elif self.timer <= 20:
            frame = self.frames[1]
        elif self.timer <= 30:
            frame = self.frames[2]
        elif self.timer <= 40:
            frame = self.frames[3]
        else:
            self.timer = 0
            new_action = 'idle'
            frame = self.frames[0]
        self.timer += 1
        self.screen.blit(frame, (0,0))
        return new_action