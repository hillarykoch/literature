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
from literature.view.ask_display import ask_display
from literature.view.text_input import TextInput

from literature.game.people import Player, Team
from literature.game.cards import Card, Deck, Hand
from literature.game.literature import Literature # should fix this naming

#--------------------------------------------------------------------------------
# Initialize pygame
pygame.init()

# Make black background and draw table
screen.fill((0, 0, 0))
screen.blit(table, (0,0))

# flip the display
pygame.display.flip()

#--------------------------------------------------------------------------------
# Blit players and the sizes of the their hands
GAME_FONT = pygame.freetype.Font("literature/images/fonts/Montserrat-Regular.ttf", 16)
GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] - 100), game.teams[0].team_name, (150, 150, 150))
for (i, plr) in enumerate(game.teams[0].roster):
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20 - 100), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1]), game.teams[1].team_name, (150, 150, 150))
for (i, plr) in enumerate(game.teams[1].roster):
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

# Run until the user asks to quit
running = True

ok_button.deactivate()
for button in buttons:
    screen.blit(button.surf, button.rect)

#--------------------------------------------------------------------------------
# Draw hand of the current player
cur_player_idx = 0
still_playing = True
# cur_player_idx = (cur_player_idx + 1) % Literature.NUM_PLAYERS
hand_display = Hand_display(game.cur_player.hand)
game.cur_player.guessed_correctly = True

while (running) and (game.cur_player.still_playing()) and (game.cur_player.guessed_correctly): 

    # Blit the hand
    for c in range(hand_display.num_cards):
        t, l = hand_display.card_displays[c].rect.topleft
        screen.blit(card_outline, (t - 1, l - 1))
        screen.blit(hand_display.card_displays[c].surf, hand_display.card_displays[c].rect)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.update(pygame.mouse.get_pos())
            
            hand_display.update(event)
        
        # This block is executed once for each MOUSEBUTTONDOWN event.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                # `event.pos` is the mouse position.
                if ask_button.rect.collidepoint(event.pos):
                    finished = ask_display(game, hand_display, GAME_FONT)
                    
                    if not finished:
                        running = False
                
                elif claim_button.rect.collidepoint(event.pos):
                    GAME_FONT.render_to(screen, (FAR_LEFT + 200, ask_button.rect.top - 200), "You clicked the claim button!!!", (150, 150, 150))

    #--------------------------------------------------------------------------------
    # Blit all the sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #--------------------------------------------------------------------------------
    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
