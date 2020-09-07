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
from literature.view.my_text_input import Text_box

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
#name_input = Text_box(box_size = (200, 35), box_color = (0,0,0), text_color=(225,225,225), cursor_color=(225,225,225), max_string_length=14)
#
## Blit the text surface to the screen
#name_input.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
#screen.blit(name_input.surface, name_input.rect)
#
#clock = pygame.time.Clock()



# flip the display
pygame.display.flip()

running = True
while running:
    events = pygame.event.get()
    #name_input.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    #screen.blit(name_input.surface, ( (SCREEN_WIDTH - name_input.rect.width) / 2, (SCREEN_HEIGHT - name_input.rect.height) / 2))

#    if name_input.update(events):
#        username = name_input.get_text()
#        name_input.clear_text()
#    else:
#        # Blit the text surface to the screen
#        screen.blit(name_input_surface, (name_input_rect.left, name_input_rect.top))

    #--------------------------------------------------------------------------------
    # Flip the display
    pygame.display.flip()
    #clock.tick(30)

# Done! Time to quit.
pygame.quit()