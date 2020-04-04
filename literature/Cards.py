from random import sample

class Card:
    def __init__(self, value, suit = ["spades", "hearts", "diamonds", "clubs", "Big", "Little"]):
        if value in range(0,14,1): # 0 = Joker, 
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

class Hand:
    def __init__(self):
        self.cards = [None] * 9
    def show(self):
        [ crd.get_card_name() for crd in self.cards ]
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
            if card.get_card_name() in [ crd.get_card_name() for crd in self.cards ]:
                return True
            else:
                return False
        else:
            print('card must be a Card.')
            raise ValueError
    def contains_rng(self, card):
        if card.rng == 'eights_and_jokers':
            if 'eights_and_jokers' in [ crd.rng for crd in self.cards ]:
                return True
            else:
                return False
        else:
            if any(([card.rng in crd.rng for crd in self.cards]) and 
                    ([card.suit in crd.suit for crd in self.cards])):
                return True
            else:
                return False
    # need to and something to sort cards 

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
        for crd in self.cards:
            print(crd.get_card_name())