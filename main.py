#!/usr/bin/env python3

# could import *, but explicit better than implicit
from literature.game.people import Player, Team
from literature.game.cards import Card, Deck, Hand
from literature.game.literature import Literature # should fix this naming

from literature.comms.console_comms import ConsoleComms 
from literature.comms.network_comms import NetworkComms 

def main():
    team1 = Team('Planet Express Crew', 1)
    team2 = Team('City of Townsville Chaos Squad', 2)
    
    p1 = Player('Leela', 1, 1)
    p2 = Player('Zoidberg', 1, 2, comms=NetworkComms())
    p3 = Player('Philip J. Fry', 1, 3)
    
    p4 = Player('Mojo Jojo', 2, 1, comms=NetworkComms())
    p5 = Player('Him', 2, 2)
    p6 = Player('Fuzzy Lumpkins', 2, 3)
    
    team1.add_teammate(p1)
    team1.add_teammate(p2)
    team1.add_teammate(p3)
    team1.show_roster()
    print()
    
    team2.add_teammate(p4)
    team2.add_teammate(p5)
    team2.add_teammate(p6)
    team2.show_roster()
    print()
    
    game = Literature(team1, team2)
    game.play_game()
    

# info: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    main()
