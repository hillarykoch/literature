import pygame
from pygame.locals import *

from literature.game.people import Player, Team
from literature.game.cards import Card, Deck, Hand
from literature.game.literature import Literature # should fix this naming

from literature.view.button import Button

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


#--------------------------------------------------------------------------------
# Create teams (until we can handle multiple people joining)
team1 = Team('Planet Express Crew', 1)
team2 = Team('City of Townsville Chaos Squad', 2)

team1.add_teammate(Player('Leela', 1, 1))
team1.add_teammate(Player('Zoidberg', 1, 2))
team1.add_teammate(Player('Philip J. Fry', 1, 3))

team2.add_teammate(Player('Mojo Jojo', 2, 1))
team2.add_teammate(Player('Him', 2, 2))
team2.add_teammate(Player('Fuzzy Lumpkins', 2, 3))

player = team2.roster[2]

#--------------------------------------------------------------------------------
# Create the buttons
ask_button = Button("literature/images/buttons/ask.png", BUTTON_WIDTH, BUTTON_HEIGHT)
claim_button = Button("literature/images/buttons/claim.png", BUTTON_WIDTH, BUTTON_HEIGHT)

# Add mouse hover versions of the button
ask_button.hover("literature/images/buttons/ask_hover.png")
claim_button.hover("literature/images/buttons/claim_hover.png")

# Set black to transparent
ask_button.set_transparency((0,0,0), hover = True)
claim_button.set_transparency((0,0,0), hover = True)

# Adjust placement of the buttons
ask_button.place((SCREEN_HEIGHT - CARD_HEIGHT - 2 * BUTTON_HEIGHT - 55, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))
claim_button.place((SCREEN_HEIGHT - CARD_HEIGHT - BUTTON_HEIGHT - 50, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))

# Card outlines
card_outline = pygame.Surface((CARD_WIDTH + 2, CARD_HEIGHT + 2))
pygame.draw.rect(card_outline, (0,0,0), card_outline.get_rect())