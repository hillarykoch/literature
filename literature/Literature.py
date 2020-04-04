from .Cards import Deck, Hand
from .People import Team

class Literature:
    def __init__(self, team1, team2):
        self.deck = Deck()
        self.deck.shuffle()
        self.deal(team1, team2)
    def deal(self, team1, team2):
        counter = 0
        for tm in [team1, team2]:
            for plr in tm.roster:
#                plr.hand = [ self.deck.cards[i] for i in range(counter, counter + 9) ]
#                for i in range(9):
#                    plr.hand[i] = self.deck.cards[range(counter, counter + 9)[i]]
#                    counter += 9
