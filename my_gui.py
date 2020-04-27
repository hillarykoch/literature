# External
from copy import copy
from random import sample # for testing
 
# pygame
import pygame
import pygame.freetype

from pygame.locals import (
    RLEACCEL,
    MOUSEBUTTONDOWN,
    QUIT,
    BLEND_SUB
)

# literature
from literature.view.global_constants import *
from literature.view.button import Button
from literature.view.hand_display import Hand_display, Card_display
from literature.view.text_input import TextInput

from literature.game.people import Player, Team
from literature.game.cards import Card, Deck, Hand
from literature.game.literature import Literature # should fix this naming

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

# Deals the cards
game = Literature(team1, team2)

#--------------------------------------------------------------------------------
# Initialize pygame
pygame.init()

# set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Fill the background with black
screen.fill((0, 0, 0)) 

# Add the table as the background
table = pygame.image.load("literature/images/table/table.png").convert()
table.set_colorkey((255, 255, 255), RLEACCEL)
table = pygame.transform.scale(table, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(table, (0,0))

# flip the display
pygame.display.flip()


# Make font
GAME_FONT = pygame.freetype.Font("literature/images/fonts/Montserrat-Regular.ttf", 16)

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
ask_button.place((SCREEN_HEIGHT - CARD_HEIGHT - 2 * BUTTON_HEIGHT - 55, FAR_LEFT))
claim_button.place((SCREEN_HEIGHT - CARD_HEIGHT - BUTTON_HEIGHT - 50, FAR_LEFT))

screen.blit(ask_button.img, ask_button.rect)
screen.blit(claim_button.img, claim_button.rect)


#--------------------------------------------------------------------------------
# Draw hand of the current player
cur_player = game.teams[1].roster[0]

# Draw card outlines
card_outline = pygame.Surface((CARD_WIDTH + 1, CARD_HEIGHT + 1))
pygame.draw.rect(card_outline, (0,0,0), card_outline.get_rect())
hand_display = Hand_display(cur_player.hand)

# Run until the user asks to quit
running = True

while running:
    # Blit the buttons
    screen.blit(ask_button.img, ask_button.rect)
    screen.blit(claim_button.img, claim_button.rect)
    
    if ask_button.rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(ask_button.hover_img, ask_button.rect)
    elif claim_button.rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(claim_button.hover_img, claim_button.rect)

    # Blit players and the sizes of the their hands
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.top - 200), game.teams[0].team_name, (150, 150, 150))
    for (i, plr) in enumerate(game.teams[0].roster):
        GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.top + (i+1) * 20 - 200), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.top - 100), game.teams[1].team_name, (150, 150, 150))
    for (i, plr) in enumerate(game.teams[1].roster):
        GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.top + (i+1) * 20 - 100), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

    # Blit the cards
    for c in range(hand_display.num_cards):
        t, l = hand_display.card_displays[c].rect.topleft
        screen.blit(card_outline, (t - 1, l - 1))

        # This will actually be for ask a card, not for your own hand-----------------------
        if hand_display.card_displays[c].rect.collidepoint(pygame.mouse.get_pos()):
            card_copy = copy(hand_display.card_displays[c].img)
            fill = card_copy.fill((150, 150, 150), special_flags = BLEND_SUB)
            fill.top = hand_display.card_displays[c].rect.top
            fill.left = hand_display.card_displays[c].rect.left
            screen.blit(card_copy, fill)
        else:
            screen.blit(hand_display.card_displays[c].img, hand_display.card_displays[c].rect)


    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # This block is executed once for each MOUSEBUTTONDOWN event.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                # `event.pos` is the mouse position.
                if ask_button.rect.collidepoint(event.pos):
                    GAME_FONT.render_to(screen, (FAR_LEFT + 200, ask_button.rect.top - 200), "You clicked the ask button!!!", (150, 150, 150))
                
                elif claim_button.rect.collidepoint(event.pos):
                    GAME_FONT.render_to(screen, (FAR_LEFT + 200, ask_button.rect.top - 200), "You clicked the claim button!!!", (150, 150, 150))

    #--------------------------------------------------------------------------------
    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
