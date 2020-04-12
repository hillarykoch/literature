# external
# Can learn to creates styles using module prompt_toolkil
#   See: https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html
from examples import custom_style_2, custom_style_3
from PyInquirer import prompt

from literature.comms.icomms import IComms
from literature.game.global_queries import initialize_move_question
from literature.game.global_queries import pick_opponent_question

class ConsoleComms(IComms):
    def __init__(self):
        pass

    def parse(self, data, case, **opposing_team):
        if case == 0:
            return data['turn_type'].split()[0].lower() # returns 'ask' and 'claim'
        elif case == 3:
            for plr in opposing_team['opposing_team'].roster:
                if data['turn_type'] == plr.name:
                    return plr
            print("Never found the player you wanted to ask.")
            raise NameError
        else:
            return data

    def get_data(self, case, **choices):
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
        elif case == 3:
            pick_opponent_question[0]["choices"] = choices["choices"]

            # Which player to ask?
            data = prompt(pick_opponent_question, style=custom_style_2)
            return data
        else:
            return self.parse("got this from stdin")

        # this'll be what it is, but for testing see above
        # return self.parse(input()) 
    def send_data(self, data):
        return f"sent {data} over stdin"
