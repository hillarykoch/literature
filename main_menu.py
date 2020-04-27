# External
from random import sample # for testing
 
# pygame
import pygame
import pygame.freetype

from pygame.locals import (
    RLEACCEL,
    MOUSEBUTTONDOWN,
    QUIT
)

# literature
from literature.view.global_constants import *
from literature.view.text_input import TextInput

from literature.game.people import Player, Team
from literature.game.literature import Literature # should fix this naming


# Initialize pygame
pygame.init()

#--------------------------------------------------------------------------------
# Sign in menu

# set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Fill the background with black
screen.fill((0, 0, 0)) 

# Add the table as the background
table = pygame.image.load("literature/images/table/table.png").convert()
table.set_colorkey((255, 255, 255), RLEACCEL)
table = pygame.transform.scale(table, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(table, (0,0))

#--------------------------------------------------------------------------------
# Add the title
# Make font
MENU_FONT = pygame.freetype.Font("literature/images/fonts/Confetti_Stream.ttf", 175)

# create a text suface object, center the rect
title, title_rect = MENU_FONT.render("Literature", (225,225,225)) 
title_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 )
screen.blit(title, title_rect)


#--------------------------------------------------------------------------------
# Add input getter
# Create TextInput objects from team name and player name
team_input = TextInput(text_color=(225,225,225), cursor_color=(225,225,225), max_string_length=14)
name_input = TextInput(text_color=(225,225,225), cursor_color=(225,225,225), max_string_length=14)
clock = pygame.time.Clock()

# Blit the text surface to the screen
screen.blit(team_input.get_surface(), (250, 450))
screen.blit(name_input.get_surface(), (250, 490))

# flip the display
pygame.display.flip()

running = True
while running:
    # Did the user click the window close button?
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if team_input.update(events):
        username = team_input.get_text()
    elif name_input.update(events):
        username = name_input.get_text()
    else:
        # Blit the text surface to the screen
        screen.blit(team_input.get_surface(), (250, 450))
        screen.blit(name_input.get_surface(), (250, 490))

    #--------------------------------------------------------------------------------
    # Flip the display
    pygame.display.flip()
    clock.tick(30)

# Done! Time to quit.
pygame.quit()