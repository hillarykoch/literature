from literature.game.cards import Card, Hand
from literature.comms.console_comms import ConsoleComms 

# external
from random import sample

# I don't think I will need team_number and player_number to be passed
#   but will probably need to assign them
class Player:
    def __init__(self, name, team_number, 
            player_number, 
            comms = ConsoleComms(),
            CPU = False):
        self.name = name
        self.hand = Hand()

        """ For tracking if it is still a Player's turn.
            Set this to True at the start of a turn so that a Player may take multiple guesses.
            Set it to False if the player fails to obtain a card to stop the turn.
        """  
        self.guessed_correctly = False

        self.comms      = comms
        self.CPU_status = CPU

        self.deny_phrases = ['Nice try!', 
                'I don\'t think so!', 
                'Noooope.', 
                'Go feesh!', 
                'You asked me that last time.'
            ]

        self.hand_over_phrases = ['Yeah....', 
                '*Heavy sigh*', 
                'You\'re cheating!', 
                'How did you know?', 
                'Ok but I\'m gonna get you back, you little stinker....you just wait.'
            ]

        self.proclamations = ['Yeet', 
                'Scooooooop!', 
                'OFY', 
                'We\'re on a roll, baby.'
            ]

        if team_number in [1, 2]:
            self.team_number = team_number
        else:
            print("There can only be Team 1 and Team 2.")
            raise ValueError

        if player_number in [1, 2, 3]:
            self.player_number = player_number
        else:
            print("There can only be player numbers 1, 2, and 3.")
            raise ValueError

        self.position = self.player_number * 2 - 3 + self.team_number

#    def get_input(self, case):
#        return self.comms.get_data()

    def change_player_number(self, new_number):
            if new_number in [1, 2, 3]:
                self.player_number = new_number
                self.position = self.player_number * 2 - 3 + self.team_number
            else:
                print("There can only be player numbers 1, 2, and 3.")
                raise ValueError

    def still_playing(self):
        return (len(self.hand.cards) > 0)

    def hand_over_card(self, card):
        if isinstance(card, Card):            
            self.hand.remove_card(card)
        else:
            print('card must be a Card.')
            raise ValueError

    def has_card(self, card):
        return self.hand.contains_card(card=card)
        
    def has_rng(self, card):
        return self.hand.contains_rng(card)

    def ask_for_card(self, opponent, card):
        if opponent.team_number == self.team_number:
            print("You can't ask your own team member for a card.")
            raise ValueError
        elif self.has_card(card):
            print("You can't ask for a card you already have.")
            raise ValueError
        elif not self.has_rng(card):
            print("You can only ask for cards in a range that you possess.")
            raise ValueError
        else:
            print('\n' + self.name + ' asks ' + opponent.name + ', \'Do you have the ' + card.get_card_name() + '?\n')
            if opponent.has_card(card):
                print('\n' + opponent.name + ' says \'' + sample(self.hand_over_phrases, 1)[0] + '\'\n')
                print('\n' + self.name + ' says \'' + sample(self.proclamations, 1)[0] + '\'\n')
                opponent.hand_over_card(card)
                self.hand.add_card(card)
                self.hand.sort()
            else:
                self.guessed_correctly = False
                print('\n' + opponent.name + ' says \'' + sample(self.deny_phrases, 1)[0] +'\'\n')

    ### This isn't complete ---------------------------------------------------------
    def claim(self, **kwargs): # rng, suit, claim_dict
        """if someone passes eights_and_jokers, but also a suit,
            we ignore suit and just go to eights_and_jokers"""
        if kwargs["rng"] == "eights_and_jokers": 
            # prompts for different ranges might be different
            print(self.name + " is claiming the Eights and Jokers.")
        elif kwargs["suit"] in ["diamonds", "clubs", "hearts", "spades"]:
            if kwargs["rng"] not in ["low", "high"]:
                print('If the suit is diamonds, clubs, hearts, or spades, then \'low\' or \'high\' must be specified.')
                raise ValueError
            else:
                print(self.name + " is claiming the " + kwargs["rng"] + " " + kwargs["suit"] + ".")
        else:
            print("You didn't specify a compatible suit and card range.")
            raise ValueError

        # grab current team, opposing team
        cur_team = kwargs["teams"][self.team_number - 1]
        opp_team = kwargs["teams"][self.team_number % 2]

        # Now, check to see if Player guessed correctly------------------
        
        # tracks number of correctly claimed cards. Needs to reach 6
        claimed_correctly = 0

        # Track number of claimed cards that belong to the other team
        claimed_but_with_opponents = 0

        # For each player on the team
        for plr, c in kwargs["claim_dict"].items():
            # If the player supposedly has any cards
            if len(c) > 0:
                for tm in cur_team.roster:
                    # Find the current player
                    if tm.name == plr:
                        # find the card
                        if tm.hand.contains_card(card_name=c):
                            claimed_correctly += 1

                        # If the claim was wrong, find out if that card is in the hands of an opposing teammate
                        elif any([ plr.hand.contains_card(card_name = c) for plr in opp_team.roster ]):
                            claimed_but_with_opponents += 1

        # Need to update the score accordingly, based on these results
        # Need to remove claimed cards from deck and hands
                        
        pass
                            





class Team:
    def __init__(self, team_name, team_number):
        self.team_name = team_name
        self.total_teammates = 0
        self.roster = [None] * 3

        if team_number in [1, 2]:
            self.team_number = team_number
        else:
            print("There can only be Team 1 and Team 2.")
            raise ValueError

    def show_roster(self):
        [ print(plr.name) for plr in self.roster ]

    def add_teammate(self, player):
        if isinstance(player, Player):
            if self.total_teammates < 3:
                self.roster[self.total_teammates] = player
                self.total_teammates += 1
            else:
                print(self.team_name + ' is already full!')
                raise ValueError
        else:
            print('player must be of class Player.')
            raise ValueError
