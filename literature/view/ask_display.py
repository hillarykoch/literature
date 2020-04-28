import pygame
import pygame.freetype

from copy import copy

from literature.view.global_constants import *
from literature.view.button import Button
from literature.view.hand_display import Choice_display

#--------------------------------------------------------------------------------
# Define a display when opponent is selecting cards
def ask_display(game, hand_display, GAME_FONT):
    # Blit the table back to the screen
    screen.blit(table, (0,0))

    # Blit the greyed out buttons
    screen.blit(ask_button.hover_img, ask_button.rect)
    screen.blit(claim_button.hover_img, claim_button.rect)

    # Blit players and the sizes of the their hands
    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] - 100), game.teams[0].team_name, (150, 150, 150))
    for (i, plr) in enumerate(game.teams[0].roster):
        GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20 - 100), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

    GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1]), game.teams[1].team_name, (150, 150, 150))
    for (i, plr) in enumerate(game.teams[1].roster):
        GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

    pygame.display.flip()

    #--------------------------------------------------------------------------------------------
    # This is game logic from the Literature class, pasted in here for now (replaced self with game)
    opposing_team = game.teams[player.team_number % 2]
    choices = [ plr.name if plr.still_playing() else None for plr in opposing_team.roster ]

    candidate_cards = []
    for c in game.deck.cards:
        for s in player.hand.current_rngs():
            spl = s.split('-')
            cur_rng, cur_suit = spl

            if cur_rng == 'eights_and_jokers' and cur_rng == c.rng and not player.has_card(c):
                candidate_cards.append(c)
            elif c.rng == cur_rng and c.rng != 'eights_and_jokers' and c.suit == cur_suit and not player.has_card(c):
                candidate_cards.append(c)

    # sort the list
    ranks = [c.get_suit_rank() for c in candidate_cards]
    vals = [c.get_value_rank() for c in candidate_cards]

    print([c.get_card_name() for c in candidate_cards])

    candidate_cards = [c for _, _, c in sorted( # took out get_card_name(c) and changed to c.
        zip(ranks, vals, candidate_cards), key=lambda x: (x[0], x[1]))]

    print([c.get_card_name() for c in candidate_cards])
    choice_display = Choice_display(candidate_cards)

    asking = True
    while asking:
        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                return False

            elif event.type == MOUSEMOTION:
                # Blit the candidate cards
                for c in range(choice_display.num_cards):
                    t, l = choice_display.card_displays[c].rect.topleft
                    screen.blit(card_outline, (t - 1, l - 1))

                    if choice_display.card_displays[c].rect.collidepoint(pygame.mouse.get_pos()) and not \
                                    any([ choice_display.card_displays[x].rect.collidepoint(pygame.mouse.get_pos()) for x in range(c+1, choice_display.num_cards)]):

                        card_copy = copy(choice_display.card_displays[c].img)
                        fill = card_copy.fill((150, 150, 150), special_flags = BLEND_SUB)
                        fill.top = choice_display.card_displays[c].rect.top
                        fill.left = choice_display.card_displays[c].rect.left
                        screen.blit(card_copy, fill)
                    else:
                        screen.blit(choice_display.card_displays[c].img, choice_display.card_displays[c].rect)

                # Blit the hand
                for c in range(hand_display.num_cards):
                    t, l = hand_display.card_displays[c].rect.topleft
                    screen.blit(card_outline, (t - 1, l - 1))
                    screen.blit(hand_display.card_displays[c].img, hand_display.card_displays[c].rect)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for c in range(choice_display.num_cards):
                        # If the card is clicked, blit the card to the front
                        if choice_display.card_displays[c].rect.collidepoint(event.pos) and not \
                            any([ choice_display.card_displays[x].rect.collidepoint(event.pos) for x in range(c+1, choice_display.num_cards)]):
                            t, l = choice_display.card_displays[c].rect.topleft
                            screen.blit(card_outline, (t - 1, l - 1))
                            screen.blit(choice_display.card_displays[c].img, choice_display.card_displays[c].rect)

        #--------------------------------------------------------------------------------
        # Flip the display
        pygame.display.flip()
    

