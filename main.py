#!/usr/bin/env python3

# could import *, but explicit better than implicit
from literature.game.people import Player, Team
from literature.game.cards import Card, Deck, Hand
from literature.game.literature import Literature # should fix this naming

from literature.comms.console_comms import ConsoleComms 
from literature.comms.network_comms import NetworkComms 
from literature.comms.gui_comms import GUIComms

from literature.view.button import Button
from literature.view.global_constants import *

import pygame
import pygame.freetype
from pygame.locals import *

def mmmain():
    # Deals the cards
    game = Literature(team1, team2)

    #----------------------------------------------------------------
    # Play in GUI mode
    #----------------------------------------------------------------
    # shouldnt need to be passing all these buttons etc.... its a bandaid for now
    game.play_game(GUI=True, GAME_FONT = GAME_FONT, ask_button = ask_button, claim_button = claim_button, ok_button = ok_button, buttons = buttons, all_sprites = all_sprites)
    

if __name__ == "__main__":
    #--------------------------------------------------------------------------------
    # Initialize pygame
    #--------------------------------------------------------------------------------
    pygame.init()

    # Create GAME_FONT
    GAME_FONT = pygame.freetype.Font("literature/images/fonts/Montserrat-Regular.ttf", 16)

    #----------------------------------------------------------------
    # Set up buttons
    #----------------------------------------------------------------
    ## Create sprite groups for the ask and claim buttons
    ask_button = Button("literature/images/buttons/ask.png", BUTTON_WIDTH, BUTTON_HEIGHT)
    claim_button = Button("literature/images/buttons/claim.png", BUTTON_WIDTH, BUTTON_HEIGHT)
    ok_button = Button("literature/images/buttons/ok.png", BUTTON_WIDTH, BUTTON_HEIGHT)

    # Add mouse hover versions of the button
    ask_button.hover("literature/images/buttons/ask_hover.png")
    claim_button.hover("literature/images/buttons/claim_hover.png")
    ok_button.hover("literature/images/buttons/ok_hover.png")

    # Set black to transparent
    ask_button.set_transparency((0,0,0), hover = True)
    claim_button.set_transparency((0,0,0), hover = True)
    ok_button.set_transparency((0,0,0), hover = True)

    # Adjust placement of the buttons
    ok_button.place((SCREEN_HEIGHT - CARD_HEIGHT - 3 * BUTTON_HEIGHT - 60, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))
    ask_button.place((SCREEN_HEIGHT - CARD_HEIGHT - 2 * BUTTON_HEIGHT - 55, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))
    claim_button.place((SCREEN_HEIGHT - CARD_HEIGHT - BUTTON_HEIGHT - 50, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))

    ## Put everything in a button sprite group
    buttons = pygame.sprite.Group()

    buttons.add(ok_button)
    buttons.add(ask_button)
    buttons.add(claim_button)

    # A sprite group for all sprites
    all_sprites = pygame.sprite.Group()

    for button in buttons:
        all_sprites.add(button)

    #----------------------------------------------------------------
    # Create players, teams, and the game
    #----------------------------------------------------------------
    p1 = Player('Leela', 1, 1)
    p2 = Player('Zoidberg', 1, 2)
    p3 = Player('Philip J. Fry', 1, 3)
    
    p4 = Player('Mojo Jojo', 2, 1)
    p5 = Player('Him', 2, 2)
    p6 = Player('Fuzzy Lumpkins', 2, 3)

    # Create teams
    team1 = Team('Planet Express Crew', 1)
    team2 = Team('City of Townsville Chaos Squad', 2)

    team1.add_teammate(p1)
    team1.add_teammate(p2)
    team1.add_teammate(p3)
    team1.show_roster()
    
    team2.add_teammate(p4)
    team2.add_teammate(p5)
    team2.add_teammate(p6)
    team2.show_roster()

    mmmain()

