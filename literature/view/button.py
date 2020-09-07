import pygame

from pygame.locals import (
    RLEACCEL
)

from literature.view.global_constants import *

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, BUTTON_WIDTH, BUTTON_HEIGHT):
        super(Button, self).__init__()
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT

        self.reg_surf = pygame.image.load(image_path).convert()
        self.reg_surf = pygame.transform.scale(self.reg_surf, (BUTTON_WIDTH, BUTTON_HEIGHT))
        
        self.surf = self.reg_surf
        self.rect = self.surf.get_rect()

        self.deactivated = False
        #self.selected = False

    # Add a mouse hover image
    def hover(self, image_path):
        self.hover_surf = pygame.image.load(image_path).convert()
        self.hover_surf = pygame.transform.scale(self.hover_surf, (self.width, self.height))
    
    def set_transparency(self, rgb, hover = False):
        self.surf.set_colorkey(rgb, RLEACCEL)

        if hasattr(self, "hover_surf"):
            self.hover_surf.set_colorkey(rgb, RLEACCEL)

    def place(self, topleft):
        self.rect.top, self.rect.left = topleft

    def deactivate(self):
        self.surf = self.hover_surf
        self.deactivated = True

    def reactivate(self):
        self.surf = self.reg_surf
        self.deactivated = False

    def update(self, mouse_pos):
        if not self.deactivated:
            if self.rect.collidepoint(mouse_pos):
                self.surf = self.hover_surf
            else:
                self.surf = self.reg_surf

class TextButton(pygame.sprite.Sprite):
    def __init__(self, txt, font, hoverfont, color, hovercolor, player):
        super(TextButton, self).__init__()
        self.regsurf, _ = font.render(txt, fgcolor=color)
        self.regrect = self.regsurf.get_rect()

        self.hoversurf, _ = hoverfont.render(txt, fgcolor=hovercolor)
        self.hoverrect = self.hoversurf.get_rect()

        self.rect = self.regrect
        self.surf = self.regsurf
        self.deactivated = False
        self.selected = False

        self.player = player
        self.team = self.player.team_number
        

    # Add a mouse hover image
    def hover(self, image_path):
        self.rect = self.hoverrect
    
    def place(self, topleft):
        self.rect.topleft = topleft

    def deactivate(self):
        self.surf = self.hoversurf
        self.deactivated = True

    def reactivate(self):
        self.surf = self.regsurf
        self.deactivated = False

    def update(self, event):
        if not self.deactivated:
            if not self.selected:
                if event.type == MOUSEMOTION:
                    if self.rect.collidepoint(pygame.mouse.get_pos()):
                        self.surf = self.hoversurf
                    else:
                        self.surf = self.regsurf