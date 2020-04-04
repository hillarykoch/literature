from .Cards import Card
from random import sample

class Player:
    def __init__(self, name, team_number, player_number, CPU = False):
        self.name = name
        self.hand = []
        self.CPU_status = CPU
        self.deny_phrases = ['Nice try!', 'I don\'t think so!', 'Noooope.', 'Go feesh!', 'You asked me that last time.']
        self.hand_over_phrases = ['Yeah....', '*Heavy sigh*', 'You\'re cheating!', 'How did you know?', 'Ok but I\'m gonna get you back, you little stinker....you just wait.']
        self.proclamations = ['Yeet', 'Scooooooop!', 'OFY', 'We\'re on a roll, baby.']
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
    def change_player_number(self, new_number):
            if new_number in [1, 2, 3]:
                self.player_number = new_number
                self.position = self.player_number * 2 - 3 + self.team_number
            else:
                print("There can only be player numbers 1, 2, and 3.")
                raise ValueError
    def show_hand(self):
        [ crd.get_card_name() for crd in self.hand ]
    def add_card(self, card):
        if isinstance(card, Card):
            self.hand.append(card)
        else:
            print('card must be a Card.')
            raise ValueError
    def hand_over_card(self, card):
        if isinstance(card, Card):            
            self.hand.remove(card)
        else:
            print('card must be a Card.')
            raise ValueError
    def has_card(self, card):
        if isinstance(card, Card):
            if card.get_card_name() in [ crd.get_card_name() for crd in self.hand ]:
                return True
            else:
                return False
        else:
            print('card must be a Card.')
            raise ValueError
    def has_rng(self, card):
        if card.rng == 'eights_and_jokers':
            if 'eights_and_jokers' in [ crd.rng for crd in self.hand ]:
                return True
            else:
                return False
        else:
            if any(([  card.rng in crd.rng for crd in self.hand ]) and ([ card.suit in crd.suit for crd in self.hand ])):
                return True
            else:
                return False
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
                print(self.name + ' says \'' + sample(self.proclamations, 1)[0], + '\'')
                opponent.hand_over_card(card)
                self.add_card(card)
            else:
                print(opponent.name + ' says \'' + sample(self.deny_phrases, 1)[0] +'\'')


class Team:
    def __init__(self, team_name, team_number):
        self.team_name = team_name
        self.total_teammates = 0
        self.roster = {}
        if team_number in [1, 2]:
            self.team_number = team_number
        else:
            print("There can only be Team 1 and Team 2.")
            raise ValueError
    def show_roster(self):
        return self.roster
    def add_teammate(self, player):
        if isinstance(player, Player):
            if self.show_roster().get(player.position) is None:
                self.roster[player.position] = player.name
            else:
                print('Position ' + str(player.position) + ' is already taken!')
                raise ValueError
        if self.total_teammates < 3:
            self.total_teammates += 1
        else:
            print('Team ' + str(self.team_number) + ' is full!')
            raise ValueError