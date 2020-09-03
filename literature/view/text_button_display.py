import pygame

from literature.view.button import TextButton
from literature.view.global_constants import *

class TextButtonDisplay(pygame.sprite.Group):
    def __init__(self, text_buttons):
        super(TextButtonDisplay, self).__init__()
        self.buttons = text_buttons

    def button_group_update(self, event):
        if (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
            for entity in self.buttons:
                if (entity.rect.collidepoint(pygame.mouse.get_pos())) and not (entity.deactivated):
                    if not entity.selected:
                        entity.selected = True
                        entity.surf = entity.hoversurf
                    else:
                        entity.selected = False
                        entity.surf = entity.regsurf
                else:
                    entity.selected = False
                    entity.surf = entity.regsurf
        else:
            self.buttons.update(event)
