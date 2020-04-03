from .Cards import Card

class Player:
    def __init__(self, name, team_number, player_number, CPU = False):
        self.name = name
        self.hand = [None] * 9
        self.CPU_status = CPU
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
    def has_card(self, card):
        if isinstance(card, Card):
            if card.get_card_name() in [ crd.get_card_name() for crd in self.hand ]:
                return True
            else:
                return False
        else:
            print('card must be a Card.')
            raise ValueError


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