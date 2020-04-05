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

    def get_input(self):
        return self.comms.get_data()

    def change_player_number(self, new_number):
            if new_number in [1, 2, 3]:
                self.player_number = new_number
                self.position = self.player_number * 2 - 3 + self.team_number
            else:
                print("There can only be player numbers 1, 2, and 3.")
                raise ValueError

    def still_playing(self):
        return len(self.hand.cards) > 0

    def hand_over_card(self, card):
        if isinstance(card, Card):            
            self.hand.remove_card(card)
        else:
            print('card must be a Card.')
            raise ValueError

    def has_card(self, card):
        return self.hand.contains_card(card)
        
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
            print(self.name + ' asks ' + opponent.name + ', \'Do you have the ' + card.get_card_name() + '?')
            if opponent.has_card(card):
                print(opponent.name + ' says \'' + sample(self.hand_over_phrases, 1)[0] + '\'')
                print(self.name + ' says \'' + sample(self.proclamations, 1)[0] + '\'')
                opponent.hand_over_card(card)
                self.hand.add_card(card)
                self.hand.sort()
            else:
                print(opponent.name + ' says \'' + sample(self.deny_phrases, 1)[0] +'\'')


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
