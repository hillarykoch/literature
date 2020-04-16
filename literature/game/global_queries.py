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

which_teammate_has_which_cards_question = [
    {
        'type': 'checkbox',
        #'type': 'list',
        'name': 'claimed',
        'message': 'Select which teammates you believe are holding which cards',
        'choices': []#,
        #'validate': lambda answer: 'You can\'t claim that multiple players hold the same card.'\
        #    if len(answer) == 0 else True
        #'filter': lambda answer: answer if len(answer) > 0 else None
    }
]

are_you_sure_question = [
    {
        'type': 'confirm',
        'message': 'Are you sure?',
        'name': 'sureness',
        'default': True,
    }
]