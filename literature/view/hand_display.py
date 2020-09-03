from numpy import linspace
from copy import copy

import pygame
from literature.view.global_constants import *



# Card is a sprite
class Card_display(pygame.sprite.Sprite):
    def __init__(self, card):
        super(Card_display, self).__init__()
        self.card = card
        self._layer = 1
        self.selected = False

        # Associate a path to an image
        if card.value in (0, 11):
            v = "J"
        elif card.value == 12:
            v = "Q"
        elif card.value == 13:
            v = "K"
        elif card.value == 1:
            v = "A"
        else:
            v = str(card.value)
        self.image_path = "literature/images/cards/" + v + card.suit[0].upper() + ".png"

        # Load in and scale the image, then get the image rect
        self.reg_surf = pygame.image.load(self.image_path).convert()
        self.reg_surf = pygame.transform.scale(self.reg_surf, (CARD_WIDTH, CARD_HEIGHT))
        
        self.surf = self.reg_surf
        self.rect = self.surf.get_rect()

        dark_copy = copy(self.reg_surf)
        fill = dark_copy.fill((150, 150, 150), special_flags = BLEND_SUB)

        self.hover_surf = copy(self.surf)
        self.hover_surf.blit(dark_copy, fill) 


    def place(self, topleft, home_layer):
        self.rect.top, self.rect.left = topleft
        self._layer = home_layer
        self.home_layer = home_layer

    def update(self, darken=False):
        if darken:
            self.surf = self.hover_surf
        else:
            self.surf = self.reg_surf

class Hand_display(pygame.sprite.LayeredUpdates):
    def __init__(self, hand):
        super(Hand_display, self).__init__()
        self.hand = hand
        self.num_cards = len(self.hand.cards)

        # Where to draw every card
        rect_locs = list(linspace(FAR_LEFT, FAR_RIGHT, self.num_cards, dtype = int))
        self.card_displays = [None] * self.num_cards

        # Make a display for each card in the hand
        for (i, c) in enumerate(self.hand.cards):
            self.card_displays[i] = Card_display(c)
            self.card_displays[i].place((SCREEN_HEIGHT - CARD_HEIGHT - 35, rect_locs[i]), 1)
            self.add(self.card_displays[i])

    def update(self, event):
        if event.type == MOUSEMOTION:
            # change the color of the card, maybe change its layer
            for c in range(self.num_cards):
                
                if self.card_displays[c].rect.collidepoint(pygame.mouse.get_pos()) and not \
                    any([ self.card_displays[x].rect.collidepoint(pygame.mouse.get_pos()) for x in range(c+1, self.num_cards)]):
                    
                    self.card_displays[c].update(darken = True)
                
                else:
                    self.card_displays[c].update(darken = False)


# For asking for new cards
class Choice_display(pygame.sprite.LayeredUpdates):
    def __init__(self, candidate_cards):
        super(Choice_display, self).__init__()
        self.cards = candidate_cards
        self.num_cards = len(self.cards)

        # Where to draw every card
        rect_locs = list(linspace(FAR_LEFT, FAR_RIGHT, min(self.num_cards, 10), dtype = int))
        self.card_displays = [None] * self.num_cards

        # Make a display for each card in the hand
        for (i, c) in enumerate(self.cards):
            self.card_displays[i] = Card_display(c)

            self.add(self.card_displays[i])
            if i in range(10):
                self.card_displays[i].place((35, rect_locs[i]), i)
            elif i in range(10,20):
                self.card_displays[i].place((35 + int(CARD_HEIGHT * .33), rect_locs[i % 10]), i)
            elif i in range(20,30):
                self.card_displays[i].place((35 + int(CARD_HEIGHT * .67), rect_locs[i % 10]), i)
            elif i in range(30,40):
                self.card_displays[i].place((35 + int(CARD_HEIGHT * 1), rect_locs[i % 10]), i)
            elif i in range(40,50):
                self.card_displays[i].place((35 + int(CARD_HEIGHT * 1.33), rect_locs[i % 10], i))
            
            

    def update(self, event):
        if event.type == MOUSEMOTION:
            # change the color of the card, maybe change its layer
            for c in range(self.num_cards):
                
                if self.card_displays[c].rect.collidepoint(pygame.mouse.get_pos()) and not \
                    any([ self.card_displays[x].rect.collidepoint(pygame.mouse.get_pos()) for x in range(c+1, self.num_cards)]):
                    
                    self.card_displays[c].update(True)
                
                else:
                    
                    self.card_displays[c].update(False)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                c = 0
                for entity in self:
                    # If the card is clicked, blit the card to the front
                    if entity.rect.collidepoint(event.pos) and not \
                        any([ self.card_displays[x].rect.collidepoint(event.pos) for x in range(c+1, self.num_cards)]):

                        if (self.get_layer_of_sprite(entity) == self.get_top_layer()) and (entity.home_layer != self.get_top_layer()):
                            self.change_layer(entity, entity.home_layer)
                            entity.selected = False
                        elif entity.home_layer == self.get_top_layer():
                            entity.selected = not entity.selected
                        else:
                            self.move_to_front(entity)
                            entity.selected = True
                            
                    else:
                        
                        entity.selected = False
                        
                        if self.get_layer_of_sprite(entity) != entity.home_layer:
                            self.change_layer(entity, entity.home_layer)
                    
                    c += 1

