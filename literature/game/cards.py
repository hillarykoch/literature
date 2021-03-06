# external
from random import sample


class Card:
    def __init__(self, value, suit=["spades", "hearts", "diamonds", "clubs", "Big", "Little"]):
        self.SUIT_DICT = {"clubs": 1, "diamonds": 2, "spades": 3, "hearts": 4}
        if value in range(0, 14, 1):  # 0 = Joker, 11-13 = jack, queen, king
            self.value = value
        else:
            print(
                'Cards must be Ace through King or Joker (passed value not in range(0,14,1)).')
            raise ValueError

        if value in range(2, 8, 1):
            self.rng = "low"
        elif value in ([1] + list(range(9, 14, 1))):
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
        if self.value == 1:  # Ace high
            return 14
        elif self.value == 8:  # Eights before jokers
            return -1
        else:
            return self.value

    # rank suits as 1. eights_and_jokers 2. clubs 3. diamonds 4. spades 5. hearts
    def get_suit_rank(self):
        if self.rng == 'eights_and_jokers':
            return 0
        else:
            return self.SUIT_DICT[self.suit]


class Hand:
    def __init__(self):
        self.cards = []

    def show(self):
        for c in self.cards:
            print(c.get_card_name())

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

    def contains_card(self, **kwargs):

        # If it is a card object
        if kwargs.get("card", None) is not None:
            card = kwargs["card"]
            if isinstance(card, Card):
                if card.get_card_name() in [ c.get_card_name() for c in self.cards] :
                    return True
                else:
                    return False
            else:
                print('card must be a Card.')
                raise ValueError
        # If it is the name of a card object
        elif kwargs.get("card_name", None) is not None:
            card_name = kwargs["card_name"]
            if card_name in [ c.get_card_name() for c in self.cards] :
                return True
            else:
                return False
        else:
            print("You didn't pass a card in the keyword arguments.")
            raise ValueError


    def contains_rng(self, card):
        if card.rng == 'eights_and_jokers':
            if 'eights_and_jokers' in [c.rng for c in self.cards]:
                return True
            else:
                return False
        else:
            if any(([card.rng in c.rng for c in self.cards]) and
                    ([card.suit in c.suit for c in self.cards])):
                return True
            else:
                return False
    
    def current_rngs(self):
        # gives a list of ranges a Player has
        # so you know what ranges Player can ask for
        return set([ c.rng + '-' + c.suit for c in self.cards])

    def remove_rng(self, **kwargs):
        # remove any card that belongs to a specified rng/suit from the Hand
        if kwargs["rng"] == "eights_and_jokers":
            for c in self.cards:
                if c.rng == "eights_and_jokers":
                    self.remove_card(c)
        else:
            for c in self.cards:
                if c.rng == kwargs["rng"] and c.suit == kwargs["suit"]:
                    self.remove_card(c)

    # I think this might be a "Player" thing
    def sort(self):
        # Get card rankings by suit
        ranks = [c.get_suit_rank() for c in self.cards]

        # Get card rankings by value
        vals = [c.get_value_rank() for c in self.cards]

        # multisort cards first by by suit then by value
        self.cards = [c for _, _, c in sorted(
            zip(ranks, vals, self.cards), key=lambda x: (x[0], x[1]))]
        ### currently doesnt address 8/joker sorting I don't think ###


class Deck:
    def __init__(self):
        self.cards = [None] * 54
        self.generate()

    def generate(self):
        counter = 0
        for s in ["spades", "hearts", "diamonds", "clubs"]:
            for v in range(1, 14, 1):
                self.cards[counter] = Card(v, s)
                counter += 1
        self.cards[52] = Card(0, "Little")
        self.cards[53] = Card(0, "Big")

    def shuffle(self):
        idx = sample(range(54), 54)
        self.cards = [self.cards[i] for i in idx]

    def show(self):
        for c in self.cards:
            print(c.get_card_name())

    def current_rngs(self):
        # Gives a list of current ranges in the deck
        # so you know which ranges are still left to be claimed
        rng_set = set([ c.rng + '-' + c.suit for c in self.cards])

        out_rngs = []
        for pair in rng_set:
            p = pair.split('-')
            # Only want to count eights and jokers once
            if p[0] == "eights_and_jokers" and p[1] == "Big":
                out_rngs.append("Eights and Jokers")
            elif p[0] in ["low", "high"]:
                out_rngs.append(p[0].capitalize() + ' ' + p[1].capitalize())
        
        out_rngs.sort()
        return out_rngs

    """ If a range is claimed, perhaps we should remove it from the deck?
    That way, deck.show() would only show cards that are still in play"""

    def remove_rng(self, *rng, **kwargs): # suit is an optional kwarg
        if rng[0] == "eights_and_jokers":
            self.cards = [c for c in self.cards if not c.rng ==
                          "eights_and_jokers"]
        elif kwargs["suit"] in ["diamonds", "clubs", "hearts", "spades"]:
            if rng[0] not in ["low", "high"]:
                print(
                    'If the suit is diamonds, clubs, hearts, or spades, then \'low\' or \'high\' must be specified.')
                raise ValueError
            else:
                self.cards = [c for c in self.cards if not (
                    c.rng == rng[0] and c.suit == kwargs["suit"])]
        else:
            print("You didn't specify a compatible suit and card range.")
            raise ValueError
