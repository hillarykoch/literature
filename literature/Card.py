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