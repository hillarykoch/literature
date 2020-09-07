#import pygame
#from pygame.locals import *
#
#from literature.game.people import Player, Team
##from literature.game.cards import Card, Deck, Hand
#from literature.game.literature import Literature # should fix this naming
#from literature.view.button import Button
#
#from literature.view.global_constants import *
#
#
##--------------------------------------------------------------------------------
## Create teams (until we can handle multiple people joining)
#team1 = Team('Planet Express Crew', 1)
#team2 = Team('City of Townsville Chaos Squad', 2)
#
#team1.add_teammate(Player('Leela', 1, 1))
#team1.add_teammate(Player('Zoidberg', 1, 2))
#team1.add_teammate(Player('Philip J. Fry', 1, 3))
#
#team2.add_teammate(Player('Mojo Jojo', 2, 1))
#team2.add_teammate(Player('Him', 2, 2))
#team2.add_teammate(Player('Fuzzy Lumpkins', 2, 3))
#
## Deals the cards
#game = Literature(team1, team2)
#
#
##--------------------------------------------------------------------------------
## Create sprite groups for the ask and claim buttons
#
#ask_button = Button("literature/images/buttons/ask.png", BUTTON_WIDTH, BUTTON_HEIGHT)
#claim_button = Button("literature/images/buttons/claim.png", BUTTON_WIDTH, BUTTON_HEIGHT)
#ok_button = Button("literature/images/buttons/ok.png", BUTTON_WIDTH, BUTTON_HEIGHT)
#
## Add mouse hover versions of the button
#ask_button.hover("literature/images/buttons/ask_hover.png")
#claim_button.hover("literature/images/buttons/claim_hover.png")
#ok_button.hover("literature/images/buttons/ok_hover.png")
#
## Set black to transparent
#ask_button.set_transparency((0,0,0), hover = True)
#claim_button.set_transparency((0,0,0), hover = True)
#ok_button.set_transparency((0,0,0), hover = True)
#
## Adjust placement of the buttons
#ok_button.place((SCREEN_HEIGHT - CARD_HEIGHT - 3 * BUTTON_HEIGHT - 60, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))
#ask_button.place((SCREEN_HEIGHT - CARD_HEIGHT - 2 * BUTTON_HEIGHT - 55, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))
#claim_button.place((SCREEN_HEIGHT - CARD_HEIGHT - BUTTON_HEIGHT - 50, FAR_RIGHT + CARD_WIDTH - BUTTON_WIDTH))
#
#
## button is the sprite group
#buttons = pygame.sprite.Group()
#
#buttons.add(ok_button)
#buttons.add(ask_button)
#buttons.add(claim_button)
#
## A sprite group for all sprites
#all_sprites = pygame.sprite.Group()
#
#for button in buttons:
#    all_sprites.add(button)