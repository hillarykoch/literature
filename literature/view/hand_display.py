import pygame
from numpy import linspace
from literature.view.global_specifics import *

class Card_display:
    def __init__(self, card):
        self.card = card

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
        self.img = pygame.image.load(self.image_path).convert()
        self.img = pygame.transform.scale(self.img, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.img.get_rect()

    def place(self, topleft):
        self.rect.top, self.rect.left = topleft


class Hand_display:
    def __init__(self, hand):
        self.hand = hand
        self.num_cards = len(self.hand.cards)

        # Spreading the cards out left to right
        self.FAR_LEFT = 160
        self.FAR_RIGHT = SCREEN_WIDTH - self.FAR_LEFT - CARD_WIDTH

        # Where to draw every card
        rect_locs = list(linspace(self.FAR_LEFT, self.FAR_RIGHT, self.num_cards, dtype = int))
        self.card_displays = [None] * self.num_cards

        # Make a display for each card in the hand
        for (i, c) in enumerate(self.hand.cards):
            self.card_displays[i] = Card_display(c)
            self.card_displays[i].place((SCREEN_HEIGHT - CARD_HEIGHT - 35, rect_locs[i]))

