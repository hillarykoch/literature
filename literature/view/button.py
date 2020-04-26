import pygame

from pygame.locals import (
    RLEACCEL
)

from literature.view.global_constants import *

class Button:
    def __init__(self, image_path, BUTTON_WIDTH, BUTTON_HEIGHT):
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT

        self.img = pygame.image.load(image_path).convert()
        self.img = pygame.transform.scale(self.img, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.rect = self.img.get_rect()

    # Add a mouse hover image
    def hover(self, image_path):
        self.hover_img = pygame.image.load(image_path).convert()
        self.hover_img = pygame.transform.scale(self.hover_img, (self.width, self.height))
    
    def set_transparency(self, rgb, hover = False):
        self.img.set_colorkey(rgb, RLEACCEL)

        if hasattr(self, "hover_img"):
            self.hover_img.set_colorkey(rgb, RLEACCEL)

    def place(self, topleft):
        self.rect.top, self.rect.left = topleft

