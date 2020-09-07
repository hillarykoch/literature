import pygame
import pygame.freetype
from pygame.locals import *

# Define constants for the screen width and height
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 750

# Constant for card sizes
CARD_WIDTH=114
CARD_HEIGHT=162

# Constant for button sizes
BUTTON_WIDTH = 168
BUTTON_HEIGHT = 46

# Constant for card spacing
FAR_LEFT = 140
FAR_RIGHT = SCREEN_WIDTH - FAR_LEFT - CARD_WIDTH

# The drawing window, with table
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
table = pygame.image.load("literature/images/table/table.png").convert()
table.set_colorkey((255, 255, 255), RLEACCEL)
table = pygame.transform.scale(table, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Card outlines
card_outline = pygame.Surface((CARD_WIDTH + 2, CARD_HEIGHT + 2))
pygame.draw.rect(card_outline, (0,0,0), card_outline.get_rect())