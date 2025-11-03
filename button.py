import pygame.font

class Button:
    def __init__(self, game, msg, pos=1):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = 200
        self.height = 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.screen_rect.center
        self.rect.center = self.screen_rect.center

    def _prep_msg_multiple_buttons(self, msg, pos_number):
        w, h = self.screen_rect.center
        margin = 50
        positions = [w - self.width - margin, w, w + self.width + margin]
        pos = positions[pos_number]
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = pos
        self.rect.center = (positions[pos_number],h)
    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)