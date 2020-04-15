#from pprint import pprint

# external
from PyInquirer import style_from_dict, Token, prompt

initialize_move_question = [
    {
        'type': 'list',
        'name': 'turn_type',
        'message': 'What would you like to do?',
        'choices': ['Ask for a card', 'Claim a range']
    }
]

pick_opponent_question = [
    {
        'type': 'list',
        'name': 'player',
        'message': 'Who do you want to ask?', 
        'choices': []
    }
]

ask_for_card_question = [
    {
        'type': 'list',
        'name': 'card',
        'message': 'Which card do you want to ask for?', 
        'choices': []
    }
]

which_range_to_claim_question = [
    {
        'type': 'list',
        'name': 'range',
        'message': 'Which range do you want to claim?', 
        'choices': ["Eights and Jokers",\
            "Low Clubs", "High Clubs",\
                "Low Diamonds", "High Diamonds",\
                    "Low Spades", "High Spades",\
                        "Low Hearts", "High Hearts"]
    }
]