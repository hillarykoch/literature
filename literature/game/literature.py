# pygame
import pygame
import pygame.freetype

# literature
from literature.game.cards import Deck, Hand
from literature.game.people import Team
from literature.view.hand_display import Hand_display
from literature.view.hand_display import Choice_display
from literature.view.button import Button
from literature.view.ask_display import ask_display
from literature.view.global_constants import *


class Literature:
    NUM_PLAYERS = 6

    def __init__(self, team1, team2):
        self.deck = Deck()
        self.deck.shuffle()

        self.teams = [team1, team2] 
        self.ordered_players = self.order_players()
        
        # initialize the current player -- for GUI version
        self.cur_player = self.ordered_players[0][0]

        # scorekeeping
        self.score = [0, 0]
        self.dead_rngs = 0

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

    def query_player(self, player, **kwargs):
        # 0 => case 0, "What do you want to do?"
        # (claim, ask for card, see your hand, see available ranges)"
        data = player.comms.get_data(0)
        answer = player.comms.parse(data, 0)

        if answer == 'see':

            print("\n")
            player.hand.show()
            print("\n")

        elif answer == 'view':
            print(f"\n{self.teams[0].team_name}: {self.score[0]}")
            print(f"{self.teams[1].team_name}: {self.score[1]}")
            print(f"{self.dead_rngs} dead ranges\n")

        elif answer == 'check':
            cur_rngs = self.deck.current_rngs()

            print("\n")
            for r in cur_rngs:
                print(r)
            print("\n")

        # If Player wants to claim a range
        elif answer == 'claim':
            """Keep asking player for more cards and who has them
                If they are right their team gets a point
                If they are wrong, then either the deck dies (they had all the cards on their team, but didnt know which players had them)
                    or the opposing team gets the point
                Then range can be removed from the deck
            """
            print(f"\n{player.name} is claiming a range.\n")

            # 1 => case 1: "If claim, which suit will you claim"
            data = player.comms.get_data(1, choices=self.deck.current_rngs())
            print("\n...and that range is the " + data['range'] + ".\n")
            answer = player.comms.parse(data, 1)

            # prompt Player to find out which suit they'd like to claim
            # 2 => case2: "Given which range, which players have which cards?"
            cur_team = self.teams[player.team_number - 1]
            teammates = [ plr if plr.still_playing() else None for plr in cur_team.roster ]

            # List all candidate cards in the range to be claimed
            candidate_cards = []
            if answer[0] == 'eights_and_jokers':
                for c in self.deck.cards:
                    if c.rng == 'eights_and_jokers':
                        candidate_cards.append(c)
            else:
                for c in self.deck.cards:
                    cur_rng, cur_suit = answer
                    if c.rng == cur_rng and c.suit == cur_suit:
                        candidate_cards.append(c)

            ranks = [ c.get_suit_rank() for c in candidate_cards ]
            vals = [ c.get_value_rank() for c in candidate_cards ]
            candidate_cards = [ c.get_card_name() for _, _, c in sorted(
                zip(ranks, vals, candidate_cards), key=lambda x: (x[0], x[1])) ]

            # While loop is to let player confirm their choice before proceeding
            player_is_sure = False
            while not player_is_sure:
                claim_dict = dict()
                data = dict()
                selected = []

                # Loop over all teammates, letting player check off cards that belong to each player
                for tm in teammates:
                    # reveals card choices adaptively, so a player cannot select the same card twice
                    if data.get('claimed', None) is not None:
                        # which cards were already claimed?
                        selected += data['claimed']
                        
                        if len(selected) > 0:
                            data = player.comms.get_data(2, teammate=tm.name, choices=candidate_cards, selected=selected)
                        else: 
                            # nothing has been claimed yet
                            data = player.comms.get_data(2, teammate=tm.name, choices=candidate_cards)

                    else:
                        data = player.comms.get_data(2, teammate=tm.name, choices=candidate_cards)

                    claim_dict[tm.name] = data['claimed']

                # Enforce all 6 cards being claimed
                if sum([ len(tot_cards) for plr, tot_cards in claim_dict.items() ]) != 6:
                    print("\nYou need to claim all 6 cards in the range! Try again.\n")
                    continue
            
                # Restate choices
                print("\nSo then:\n")
                
                for tm in teammates:
                    print(tm.name + " has:")
                    if len(claim_dict[tm.name]) > 0:
                        [ print("\t " +\
                            claim_dict[tm.name][i])\
                                for i in range(len(claim_dict[tm.name])) ]
                        print("\n")
                    else:
                        print("\tnothing\n")


                # Ask the player if they're sure. If not, they can redo.
                sureness = player.comms.get_data(5)
                player_is_sure = player.comms.parse(sureness, 5)

            if answer[0] == "eights_and_jokers":
                claim_outcome = player.claim(rng=answer[0], teams=self.teams, claim_dict=claim_dict)
                self.deck.remove_rng(answer[0])

                # Remove cards from claimed ranges
                [ plr.hand.remove_rng(rng = answer[0]) for tm in self.teams for plr in tm.roster ]
            else:
                claim_outcome = player.claim(rng=answer[0], suit=answer[1], teams=self.teams, claim_dict=claim_dict)
                self.deck.remove_rng(answer[0], suit=answer[1])

                # Remove cards from claimed ranges
                [ plr.hand.remove_rng(rng = answer[0], suit = answer[1]) for tm in self.teams for plr in tm.roster ]
            
            if claim_outcome == "dead":
                self.dead_rngs += 1
            elif claim_outcome == "correct":
                print(self.score)
                print(self.teams)
                print(player.team_number)
                self.score[player.team_number - 1] += 1
            else:
                self.score[player.team_number % 2] += 1

            print("The current score is:\n")
            print(f"\t{self.teams[0].team_name}: {self.score[0]}\n")
            print(f"\t{self.teams[1].team_name}: {self.score[1]}\n")
            print(f"\nThere are currently {self.dead_rngs} dead ranges.\n")
        

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

            # If the opponent has the card, give it to Player. Otherwise, nothing happens and Player's turn is over.
            player.ask_for_card(answer1, answer2)

    def query_player_GUI(self, player, **kwargs):
        GAME_FONT = kwargs["GAME_FONT"]
        ask_button = kwargs["ask_button"]
        claim_button = kwargs["claim_button"]
        ok_button = kwargs["ok_button"]
        buttons = kwargs["buttons"]
        all_sprites = kwargs["all_sprites"]
        
        hand_display = Hand_display(player.hand)
        answer = player.comms.get_data(1, hand_display = hand_display, all_sprites = all_sprites, ask_button = ask_button, claim_button = claim_button, ok_button = ok_button, buttons = buttons)

        if answer == 'ask':

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            answer1, answer2 = player.comms.get_data(2, game = self, hand_display = hand_display, GAME_FONT = GAME_FONT,\
                ask_button = ask_button, claim_button = claim_button, ok_button = ok_button, \
                    buttons = buttons, all_sprites = all_sprites)
            
            if answer1 == False:
                running = False

            opposing_team = self.teams[self.cur_player.team_number % 2]

            print(f"\n{player.name} is going to ask for a card from a member of {opposing_team.team_name}.\n")
            print(f"\n...and that player is {answer1.name}.\n")

            # If the opponent has the card, give it to Player. Otherwise, nothing happens and Player's turn is over.
            player.ask_for_card(answer1, answer2)

            if player.guessed_correctly:
                # update ask_display and hand_display, take_turn again
                hand_display = Hand_display(player.hand)

                candidate_cards = []
                for c in self.deck.cards:
                    for s in self.cur_player.hand.current_rngs():
                        spl = s.split('-')
                        cur_rng, cur_suit = spl

                        if cur_rng == 'eights_and_jokers' and cur_rng == c.rng and not self.cur_player.has_card(c):
                            candidate_cards.append(c)
                        elif c.rng == cur_rng and c.rng != 'eights_and_jokers' and c.suit == cur_suit and not self.cur_player.has_card(c):
                            candidate_cards.append(c)

                # sort the list
                ranks = [c.get_suit_rank() for c in candidate_cards]
                vals = [c.get_value_rank() for c in candidate_cards]

                candidate_cards = [c for _, _, c in sorted(
                    zip(ranks, vals, candidate_cards), key=lambda x: (x[0], x[1]))]
                choice_display = Choice_display(candidate_cards)
                return
            else:
                # end turn, change displays entirely, etc
                print(str(player.name + "'s turn is over"))
                return


        elif answer == 'claim':
            print(f"\n{player.name} is claiming a range.\n")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            claim_dict = player.comms.get_data(3, game = self, hand_display = hand_display, GAME_FONT = GAME_FONT,\
                ask_button = ask_button, claim_button = claim_button, ok_button = ok_button, \
                    buttons = buttons, all_sprites = all_sprites)

            if claim_dict == False:
                running = False


    def take_turn(self, player, GUI=False, **kwargs):
        print(f"{player.name}'s turn\n")

        if not GUI:
            self.query_player(player)
        else:
            self.query_player_GUI(player, GAME_FONT = kwargs["GAME_FONT"], \
                            ask_button = kwargs["ask_button"], claim_button = kwargs["claim_button"], ok_button = kwargs["ok_button"], \
                                buttons = kwargs["buttons"],  all_sprites = kwargs["all_sprites"])


    def play_game(self, GUI=False, **kwargs):
        if not GUI:
            cur_player_idx = 0 
            still_playing = 1

            while(still_playing):
                cur_player = self.ordered_players[cur_player_idx][0] # offset 0 is the Player
                cur_player.guessed_correctly = True

                # The second part of the "if" condition lets a player take multiple consecutive turns if they guess correctly
                while (cur_player.still_playing()) and (cur_player.guessed_correctly): 
                    self.take_turn(cur_player)

                
                cur_player_idx = (cur_player_idx + 1) % Literature.NUM_PLAYERS

                if len(self.deck.cards) == 0:
                    still_playing = 0

                    # Report the winner, or a tie
                    if len(set(self.score)) == 1:
                        print("The game is over, and the teams tied.")
                    elif self.score[0] > self.score[1]:
                        print(f"\n{self.teams[0].team_name} beat {self.teams[1].team_name}!\n")
                    else:
                        print(f"\n{self.teams[1].team_name} beat {self.teams[0].team_name}!\n")
        else:

            cur_player_idx = 0
            GAME_FONT = kwargs["GAME_FONT"]
            ask_button = kwargs["ask_button"]
            claim_button = kwargs["claim_button"]
            ok_button = kwargs["ok_button"]
            buttons = kwargs["buttons"]
            all_sprites = kwargs["all_sprites"]

            # Make black background and draw table
            screen.fill((0, 0, 0))
            screen.blit(table, (0,0))

            #--------------------------------------------------------------------------------
            # Blit players and the sizes of the their hands
            GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] - 100), self.teams[0].team_name, (150, 150, 150))
            for (i, plr) in enumerate(self.teams[0].roster):
                GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20 - 100), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

            GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1]), self.teams[1].team_name, (150, 150, 150))
            for (i, plr) in enumerate(self.teams[1].roster):
                GAME_FONT.render_to(screen, (FAR_LEFT, ask_button.rect.center[1] + (i+1) * 20), f"{plr.name}: {len(plr.hand.cards)} cards", (225, 225, 225))

            # Run until the user asks to quit
            running = True

            ok_button.deactivate()
            for button in buttons:
                screen.blit(button.surf, button.rect)

            # Flip the display
            pygame.display.flip()

            while running:
                #--------------------------------------------------------------------------------
                # Draw hand of the current player
                still_playing = True
                self.cur_player.guessed_correctly = True

                while (running) and (self.cur_player.still_playing()) and (self.cur_player.guessed_correctly):
                    self.take_turn(self.cur_player, GUI=True, GAME_FONT = GAME_FONT, \
                        ask_button = ask_button, claim_button = claim_button, ok_button = ok_button, \
                            buttons = buttons, all_sprites = all_sprites)
                    
                    ask_button.reactivate()
                    claim_button.reactivate()
                    pygame.display.flip()
                
                cur_player_idx = (cur_player_idx + 1) % Literature.NUM_PLAYERS
                self.cur_player = self.ordered_players[cur_player_idx][0] # offset 0 is the Player
    
#    def play_game_GUI(self, **kwargs):
#        cur_player_idx = kwargs["cur_player_idx"]
#        still_playing = kwargs["still_playing"]
#
#        if still_playing:
#            self.cur_player = self.ordered_players[cur_player_idx][0] # offset 0 is the Player
#            self.cur_player.guessed_correctly = True
#
#            # The second part of the "if" condition lets a player take multiple consecutive turns if they guess correctly
#            while (self.cur_player.still_playing()) and (self.cur_player.guessed_correctly): 
#                self.take_turn(self.cur_player, GUI=True)
#            
#            #cur_player_idx = (cur_player_idx + 1) % Literature.NUM_PLAYERS
#
#            if len(self.deck.cards) == 0:
#                still_playing = 0
#
#                # Report the winner, or a tie
#                if len(set(self.score)) == 1:
#                    print("The game is over, and the teams tied.")
#                elif self.score[0] > self.score[1]:
#                    print(f"\n{self.teams[0].team_name} beat {self.teams[1].team_name}!\n")
#                else:
#                    print(f"\n{self.teams[1].team_name} beat {self.teams[0].team_name}!\n")
            


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
