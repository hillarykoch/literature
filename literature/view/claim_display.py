import pygame
import pygame.freetype

from copy import copy

from literature.view.global_constants import *
from literature.view.button import Button, TextButton
from literature.view.text_button_display import TextButtonDisplay
from literature.view.hand_display import Choice_display

#--------------------------------------------------------------------------------
# Define a display when opponent is claiming a range
def claim_display(game, hand_display, GAME_FONT, **kwargs):
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

    # Get the opposing team
    opposing_team = game.teams[game.cur_player.team_number % 2]

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

    # Create text buttons for the ranges to claim
    for (i, rng) in enumerate(game.deck.current_rngs()):
        buttontxt = rng
        b = TextButton(buttontxt, GAME_FONT, GAME_FONT, (225, 225, 225), (153, 207, 224))
        b.place((ask_button.rect.topleft[0], SCREEN_HEIGHT / 10 + (i+1) * 20))
        text_buttons.add(b)

    text_buttons = TextButtonDisplay(text_buttons)

    for button in buttons:
        screen.blit(button.surf, button.rect)

    for button in text_buttons.buttons:
        screen.blit(button.surf, button.rect)

    # Blit the hand
    for c in range(hand_display.num_cards):
        t, l = hand_display.card_displays[c].rect.topleft
        screen.blit(card_outline, (t - 1, l - 1))
        screen.blit(hand_display.card_displays[c].surf, hand_display.card_displays[c].rect)

    # Blit team names to the screen
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] - 100), game.teams[0].team_name, (150, 150, 150))
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1]), game.teams[1].team_name, (150, 150, 150))

    pygame.display.flip()

    asking = True
    while asking:
        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                return False

            elif event.type == MOUSEMOTION:
                hand_display.update(event)  
                text_buttons.button_group_update(event)

                for button in buttons:
                    button.update(pygame.mouse.get_pos())

#            elif event.type == pygame.MOUSEBUTTONDOWN:
#                mouse_pos = pygame.mouse.get_pos()
#                if (event.button == 1) and ok_button.rect.collidepoint(event.pos):
#                    
#                    # check if selected
#                    for entity in choice_display:
#                        if entity.selected:
#                            outcard = entity.card
#                    for entity in text_buttons.buttons:
#                        if entity.selected:
#                            outplayer = entity.player
#                            
#                    if ('outplayer' in locals()) and ('outcard' in locals()):
#                        return [outplayer, outcard]
#
#                elif mouse_pos[1] > (ask_button.rect.center[1] - 100):
#                    text_buttons.button_group_update(event)
#
#                else:
#                    choice_display.update(event)
#
#        # Blit the candidate cards
#        for sprite in choice_display:
#            t, l = sprite.rect.topleft
#            screen.blit(card_outline, (t-1, l-1))
#            screen.blit(sprite.surf, sprite.rect)
#
#        # Blit the hand
#        for c in range(hand_display.num_cards):
#            t, l = hand_display.card_displays[c].rect.topleft
#            screen.blit(card_outline, (t - 1, l - 1))
#            screen.blit(hand_display.card_displays[c].surf, hand_display.card_displays[c].rect)
#
#        # Blit buttons
#        for button in buttons:
#            screen.blit(button.surf, button.rect)
#
#        for button in text_buttons.buttons:
#            screen.blit(button.surf, button.rect)

        #--------------------------------------------------------------------------------
        # Flip the display
        pygame.display.flip()
    pass