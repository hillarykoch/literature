import pygame
import pygame.freetype

from copy import copy

from literature.view.global_constants import *
from literature.view.button import Button, TextButton
from literature.view.text_button_display import TextButtonDisplay
from literature.view.hand_display import Choice_display

#--------------------------------------------------------------------------------
# Define a display when opponent is selecting cards
def ask_display(game, hand_display, GAME_FONT, **kwargs):
    # Blit the table back to the screen
    screen.blit(table, (0,0))

    ask_button = kwargs["ask_button"]
    claim_button = kwargs["claim_button"]
    ok_button = kwargs["ok_button"]
    buttons = kwargs["buttons"]

    # Blit the greyed out buttons
    ok_button.reactivate()
    claim_button.deactivate()
    ask_button.deactivate()

    #--------------------------------------------------------------------------------------------
    # This is game logic from the Literature class, pasted in here for now (replaced self with game)
    opposing_team = game.teams[game.cur_player.team_number % 2]
    choices = [ plr.name if plr.still_playing() else None for plr in opposing_team.roster ]

    # Create text buttons for the players
    text_buttons = pygame.sprite.Group()
    for (i, plr) in enumerate(game.teams[0].roster):
        buttontxt = f"{plr.name}: {len(plr.hand.cards)} cards"
        b = TextButton(buttontxt, GAME_FONT, GAME_FONT, (225, 225, 225), (153, 207, 224), plr)
        b.place((FAR_LEFT, ask_button.rect.center[1]+ (i+1) * 20 - 100))
        if plr not in opposing_team.roster:
            b.deactivate()
        text_buttons.add(b)

    for (i, plr) in enumerate(game.teams[1].roster):
        buttontxt = f"{plr.name}: {len(plr.hand.cards)} cards"
        b = TextButton(buttontxt, GAME_FONT, GAME_FONT, (225, 225, 225), (153, 207, 224), plr)
        b.place((FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20))
        if plr not in opposing_team.roster:
            b.deactivate()
        text_buttons.add(b)
    
    text_buttons = TextButtonDisplay(text_buttons)

    for button in buttons:
        screen.blit(button.surf, button.rect)

    for button in text_buttons.buttons:
        screen.blit(button.surf, button.rect)

    # Blit team names to the screen
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] - 100), game.teams[0].team_name, (150, 150, 150))
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1]), game.teams[1].team_name, (150, 150, 150))

    pygame.display.flip()

    candidate_cards = []
    for c in game.deck.cards:
        for s in game.cur_player.hand.current_rngs():
            spl = s.split('-')
            cur_rng, cur_suit = spl

            if cur_rng == 'eights_and_jokers' and cur_rng == c.rng and not game.cur_player.has_card(c):
                candidate_cards.append(c)
            elif c.rng == cur_rng and c.rng != 'eights_and_jokers' and c.suit == cur_suit and not game.cur_player.has_card(c):
                candidate_cards.append(c)

    # sort the list
    ranks = [c.get_suit_rank() for c in candidate_cards]
    vals = [c.get_value_rank() for c in candidate_cards]

    candidate_cards = [c for _, _, c in sorted( # took out get_card_name(c) and changed to c.
        zip(ranks, vals, candidate_cards), key=lambda x: (x[0], x[1]))]

    choice_display = Choice_display(candidate_cards)

    asking = True
    while asking:
        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                return False

            elif event.type == MOUSEMOTION:
                hand_display.update(event)  
                choice_display.update(event)
                text_buttons.button_group_update(event)
                
                for button in buttons:
                    button.update(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (event.button == 1) and ok_button.rect.collidepoint(event.pos):
                    
                    # check if selected
                    for entity in choice_display:
                        if entity.selected:
                            outcard = entity.card
                    for entity in text_buttons.buttons:
                        if entity.selected:
                            outplayer = entity.player
                    
                    if (not outplayer is None) and (not outcard is None):
                        return [outplayer, outcard]
                    else: 
                        outcard = None
                        outplayer = None

                elif mouse_pos[1] > (ask_button.rect.center[1] - 100):
                    text_buttons.button_group_update(event)

                else:
                    choice_display.update(event)

        # Blit the candidate cards
        for sprite in choice_display:
            t, l = sprite.rect.topleft
            screen.blit(card_outline, (t-1, l-1))
            screen.blit(sprite.surf, sprite.rect)

        # Blit the hand
        for c in range(hand_display.num_cards):
            t, l = hand_display.card_displays[c].rect.topleft
            screen.blit(card_outline, (t - 1, l - 1))
            screen.blit(hand_display.card_displays[c].surf, hand_display.card_displays[c].rect)

        # Blit buttons
        for button in buttons:
            screen.blit(button.surf, button.rect)

        for button in text_buttons.buttons:
            screen.blit(button.surf, button.rect)

        #--------------------------------------------------------------------------------
        # Flip the display
        pygame.display.flip()
    

