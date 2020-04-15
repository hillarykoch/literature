# external
from pprint import pprint
# Can learn to creates styles using module prompt_toolkil
#   See: https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html
from examples import custom_style_2, custom_style_3
from PyInquirer import prompt, Separator

from copy import copy

from literature.comms.icomms import IComms

from literature.game.global_queries import initialize_move_question
from literature.game.global_queries import pick_opponent_question
from literature.game.global_queries import ask_for_card_question
from literature.game.global_queries import which_range_to_claim_question
from literature.game.global_queries import which_teammate_has_which_cards_question
from literature.game.cards import Card

class ConsoleComms(IComms):
    def __init__(self):
        pass

    def parse(self, data, case, **kwargs):
        if case == 0:
            return data['turn_type'].split()[0].lower() # returns 'ask' and 'claim'
        elif case == 1:
            # return the range and the suit
            if data['range'] == "Eights and Jokers":
                return ["eights_and_jokers"]
            else:
                return [ x.lower() for x in data['range'].split(" ") ]
        elif case == 3:
            for plr in kwargs['opposing_team'].roster:
                if data['player'] == plr.name:
                    return plr
            print("Never found the player you wanted to ask.")
            raise NameError
        elif case == 4:
            for c in kwargs['candidate_cards']:
                if c.get_card_name() == data['card']:
                    return c
            print("Never found the card you wanted to ask for.")
            raise NameError
        else:
            return data

    def get_data(self, case, **kwargs):
        """
            case: getting different data from Player, depending on which step of the game?
            i.e., case = 0: What do you want to do? (claim, ask for card)
                  case = 1: If claim, which suit will you claim
                  case = 2: Given which suit, which players have which cards?
                  case = 3: If not claim, but ask for card, who will you ask?
                  case = 4: Which card will you ask for?
        """
        if case == 0:
            data = prompt(initialize_move_question, style=custom_style_3)
            return data

        elif case == 1:

            data = prompt(which_range_to_claim_question, style=custom_style_2)
            return data

        elif case == 2:
            # Get current list of candidate cards
            list_of_dicts = [ {'name': i } for i in kwargs['choices']]

            # Append that list of the current teammate we are asking about
            choices = [ Separator(kwargs['teammate']), *list_of_dicts ]

            which_teammate_has_which_cards_question[0]['choices'] = choices
            data = prompt(which_teammate_has_which_cards_question, style=custom_style_2)
            return data

        elif case == 3:
            pick_opponent_question[0]['choices'] = kwargs['choices']

            # Which player to ask?
            data = prompt(pick_opponent_question, style=custom_style_2)
            return data

        elif case == 4:
            ask_for_card_question[0]['choices'] = kwargs['choices']

            # Which card to ask for?
            data = prompt(ask_for_card_question, style=custom_style_2)
            return data

        else:
            return self.parse("got this from stdin")

        # this'll be what it is, but for testing see above
        # return self.parse(input()) 
    def send_data(self, data):
        return f"sent {data} over stdin"
