# external
from random import sample

class Card:
    def __init__(self, value, suit = ["spades", "hearts", "diamonds", "clubs", "Big", "Little"]):
        SUIT_DICT = {"clubs": 1, "diamonds": 2, "spades": 3, "hearts": 4}
        if value in range(0,14,1): # 0 = Joker, 11-13 = jack, queen, king
            self.value = value
        else:
            print('Cards must be Ace through King or Joker (passed value not in range(0,14,1)).')
            raise ValueError

        if value in range(2,8,1):
            self.rng = "low"
        elif value in ([1] + list(range(9,14,1))):
            self.rng = "high"
        else:
            self.rng = "eights_and_jokers"

        if (self.value != 0) and (suit in ["Big", "Little"]):
            print("Only a Joker can have suit \'Big Joker\' or \'Little Joker\'")
            raise ValueError
        elif (self.value == 0) and (suit not in ["Big", "Little"]):
            print("Jokers cannot have suits spades, hearts, diamonds, or clubs.")
            raise ValueError
        else:
            self.suit = suit

    def get_card_name(self):
        if self.value == 0:
            return self.suit + " Joker"
        elif self.value == 1:
            return "Ace of " + self.suit
        elif self.value == 11:
            return "Jack of " + self.suit
        elif self.value == 12:
            return "Queen of " + self.suit
        elif self.value == 13:
            return "King of " + self.suit
        else:
            return str(self.value) + " of " + self.suit


    ############ Helpers for sorting the hand ############
    def get_value_rank(self):
        if self.value == 1: # Ace high
            return 14
        elif self.value == 8: # Eights before jokers
            return -1
        else:
            return self.value

    # rank suits as 1. eights_and_jokers 2. clubs 3. diamonds 4. spades 5. hearts
    def get_suit_rank(self):
        if self.rng == 'eights_and_jokers':
            return 0
        else:
            return SUIT_DICT[self.suit]    
        
    

class Hand:
    def __init__(self):
<<<<<<< HEAD
        self.cards = [None] * 9

    def show(self):
        [ crd.get_card_name() for crd in self.cards ]

=======
        self.cards = [ ]
    def show(self):
        for c in self.cards:
            print(c.get_card_name())
>>>>>>> 16bdf3389afda20cf3881a52d951a24b478ffc38
    def add_card(self, card):
        if isinstance(card, Card):
            self.cards.append(card)
        else:
            print('card must be a Card.')
            raise ValueError

    def remove_card(self, card):
        if isinstance(card, Card):
            self.cards.remove(card)
        else:
            print('card must be a Card.')
            raise ValueError

    def contains_card(self, card):
        if isinstance(card, Card):
            if card.get_card_name() in [ c.get_card_name() for c in self.cards ]:
                return True
            else:
                return False
        else:
            print('card must be a Card.')
            raise ValueError

    def contains_rng(self, card):
        if card.rng == 'eights_and_jokers':
            if 'eights_and_jokers' in [ c.rng for c in self.cards ]:
                return True
            else:
                return False
        else:
            if any(([  card.rng in c.rng for c in self.cards ]) and
                    ([ card.suit in c.suit for c in self.cards ])):
                return True
            else:
                return False

    # I think this might be a "Player" thing
    def sort(self):
        # Get card rankings by suit
        ranks = [ c.get_suit_rank() for c in self.cards ]

        # Get card rankings by value
        vals = [ c.get_value_rank() for c in self.cards ]

        # Sort cards by value within suit
        self.cards = [  c for _,_,c in sorted(zip(ranks, vals, self.cards), key=lambda x: (x[0], x[1])) ]
        ### currently doesnt address 8/joker sorting I don't think ###            

class Deck:
    def __init__(self):
        self.cards = [None] * 54
        self.generate()

    def generate(self):
        counter = 0
        for s in ["spades", "hearts", "diamonds", "clubs"]:
            for v in range(1,14,1):
                self.cards[counter] = Card(v, s)
                counter += 1 
        self.cards[52] = Card(0, "Little")
        self.cards[53] = Card(0, "Big")

    def shuffle(self):
        idx = sample(range(54), 54)
        self.cards = [ self.cards[i] for i in idx ]

    def show(self):
        for c in self.cards:
            print(c.get_card_name())
