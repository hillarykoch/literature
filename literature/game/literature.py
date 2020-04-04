from literature.game.cards import Deck, Hand
from literature.game.people import Team

class Literature:
    NUM_PLAYERS = 6

    def __init__(self, team1, team2):
        self.deck = Deck()
        self.deck.shuffle()

        self.teams = [team1, team2] 
        self.ordered_players = self.order_players()

        self.deal()

    def deal(self):
        for tm in self.teams:
            for plr in tm.roster:
                plr.hand = self.deck.cards[plr.position::Literature.NUM_PLAYERS]

        # make sure this worked...
        self.check_hands()

    def order_players(self):
        players = []

        for tm in self.teams:
            for plr in tm.roster:
                players.append((plr, plr.position))
        players.sort(key=lambda p: p[1]) 

        return players

    def take_turn(self, player):
        print(f"{player.name}'s turn")


    def play_game(self):
        cur_player_idx = 0 
        still_playing = 1

        while(still_playing):
            cur_player = self.ordered_players[cur_player_idx][0] # offset 0 is the Player

            if cur_player.still_playing():
                self.take_turn(cur_player)

            
            cur_player_idx = (cur_player_idx + 1) % Literature.NUM_PLAYERS

            # gotta add the end-game still_playing = 0 somewhere
            # until then, just slow down the text with this
            input()


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
