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
                plr.hand.cards = self.deck.cards[plr.position::Literature.NUM_PLAYERS]
                plr.hand.sort()

        # make sure this worked...
        self.check_hands()

    def order_players(self):
        players = []

        for tm in self.teams:
            for plr in tm.roster:
                players.append((plr, plr.position))
        players.sort(key=lambda p: p[1]) 

        return players

    def query_player(self, player):
        # 0 => case 0, "What do you want to do? (claim, ask for card)"
        data = player.comms.get_data(0)
        answer = player.comms.parse(data, 0)

        # If Player wants to claim a range
        if answer == 'claim': 
            print(f"{player.name} is claiming a range.")
            pass
        else: # Player will ask an opponent for cards
            opposing_team = self.teams[player.team_number % 2]
            print(f"\n{player.name} is going to ask for a card from a member of {opposing_team.team_name}.\n")

            """ 
                Get all players on the opposing team
                I am trying to remove players who have no cards in their hands as with this plr.still_playing() thing
                But idk if "None" works
            """
            # 3 => case 3, "If not claim, but ask for card, who will you ask?"
            choices = [ plr.name if plr.still_playing() else None for plr in opposing_team.roster ]
            data = player.comms.get_data(3, choices = choices)
            answer1 = player.comms.parse(data, 3, opposing_team = opposing_team)

            print(f"\n...and that player is {answer1.name}.\n")

            # 4 => case 4, "Which card will you ask for?"
            # Look for cards that curr_player has to determine which cards they can ask for
            candidate_cards = []
            for c in self.deck.cards:
                for s in player.hand.current_rngs():
                    spl = s.split('-')
                    cur_rng, cur_suit = spl

                    if cur_rng == 'eights_and_jokers' and cur_rng == c.rng and not player.has_card(c):
                        candidate_cards.append(c)
                    elif c.rng == cur_rng and c.suit == cur_suit and not player.has_card(c):
                        candidate_cards.append(c)

            # sort the list
            ranks = [c.get_suit_rank() for c in candidate_cards]
            vals = [c.get_value_rank() for c in candidate_cards]
            choices = [c.get_card_name() for _, _, c in sorted(
                zip(ranks, vals, candidate_cards), key=lambda x: (x[0], x[1]))]

            data = player.comms.get_data(4, choices = choices)
            answer2 = player.comms.parse(data, 4, candidate_cards = candidate_cards)
            #print(f"\n{player.name} is asking {answer1.name} for the {answer2.get_card_name()}.\n")

            """
                If the opponent has the card, give it to Player.
                Otherwise, nothing happens and Player's turn is over.
            """
            player.ask_for_card(answer1, answer2)


    def take_turn(self, player):
        print(f"{player.name}'s turn")

        print("\tAsking player what they want to do")
        self.query_player(player)

        #print(f"\tGetting input: {player.get_input()}")


    def play_game(self):
        cur_player_idx = 0 
        still_playing = 1

        while(still_playing):
            cur_player = self.ordered_players[cur_player_idx][0] # offset 0 is the Player
            cur_player.guessed_correctly = True

            # I didn't test this new "if" condition but the intent is so that a player can keep taking turns
            while (cur_player.still_playing()) and (cur_player.guessed_correctly): 
                self.take_turn(cur_player)

            
            cur_player_idx = (cur_player_idx + 1) % Literature.NUM_PLAYERS

            # gotta add the end-game still_playing = 0 somewhere
            # until then, just slow down the text with this
            #input()


################### HELPERS ####################
    def check_hands(self):
        all_cards = []
        for tm in self.teams:
            for plr in tm.roster:
                for c in plr.hand.cards:
                    all_cards.append(c)

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
