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