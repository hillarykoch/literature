from .Cards import Deck, Hand
from .People import Team

class Literature:
    NUM_PLAYERS = 6

    def __init__(self, team1, team2):
        self.deck = Deck()
        self.deck.shuffle()

        self.teams = [team1, team2] 
        self.deal()

    def deal(self):
        for tm in self.teams:
            for plr in tm.roster:
                plr.hand = self.deck.cards[plr.position::Literature.NUM_PLAYERS]

        # make sure this worked...
        self.check_hands()

################### HELPERS ####################
    def check_hands(self):
        print("Checking hands after deal")

        all_cards = []
        for tm in self.teams:
            for plr in tm.roster:
                all_cards += plr.hand

        # a set can only have one of each item.  Would be shorter than the list if any dups
        if len(all_cards) != len(set(all_cards)):
            print("Duplicates!!")
            raise ValueError


################### "DEBUG" HELPERS ####################
    def show_hands(self, team1, team2):
        print()
        print(f"{[c.get_card_name() for c in self.deck.cards]}")

        for tm in [team1, team2]:
            print()
            print(f"{tm.team_name}")
            for plr in tm.roster:
                print(f"\t{plr.name}")
                print(f"\t\t{[c.get_card_name() for c in plr.hand]}")
