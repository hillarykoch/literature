# pygame
import pygame
import pygame.freetype

# literature
from literature.comms.icomms import IComms
from literature.view.ask_display import ask_display
from literature.view.global_constants import *

class GUIComms(IComms):
    def __init__(self):
        pass 

    def parse(self, data):
        return data

    def get_data(self, case, **kwargs):
        # What does the player want to do?

        all_sprites = kwargs["all_sprites"]
        ask_button = kwargs["ask_button"]
        claim_button = kwargs["claim_button"]
        ok_button = kwargs["ok_button"]
        buttons = kwargs["buttons"]
        
        running = True
    
        if case == 1:
            hand_display = kwargs["hand_display"]

            while running:

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
                                    return 'ask'
                                
                                elif claim_button.rect.collidepoint(event.pos):
                                    return 'claim'
                            
                #--------------------------------------------------------------------------------
                # Blit all the sprites
                for entity in all_sprites:
                    screen.blit(entity.surf, entity.rect)

                #--------------------------------------------------------------------------------
                # Flip the display
                pygame.display.flip()

        elif case == 2:
            # What does the player want to ask for?

            game = kwargs["game"]
            hand_display = kwargs["hand_display"]
            GAME_FONT = kwargs["GAME_FONT"]

            plr, crd = ask_display(game, hand_display, GAME_FONT, ask_button = ask_button, claim_button = claim_button, ok_button  = ok_button, buttons = buttons)
            return [plr, crd]

    def send_data(self, data):
        return f"sent {data} over network"
