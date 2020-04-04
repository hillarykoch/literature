import literature
from literature.Cards import *
from literature.People import *
#from literature.Literature import *

team1 = Team('Planet Express Crew', 1)
team2 = Team('City of Townsville Chaos Squad', 2)

p1 = Player('Leela', 1, 1)
p2 = Player('Zoidberg', 1, 2)
p3 = Player('Philip J. Fry', 1, 3)

p4 = Player('Mojo Jojo', 2, 1)
p5 = Player('Him', 2, 2)
p6 = Player('Fuzzy Lumpkins', 2, 3)

team1.add_teammate(p1)
team1.add_teammate(p2)
team1.add_teammate(p3)
team1.show_roster()

team2.add_teammate(p4)
team2.add_teammate(p5)
team2.add_teammate(p6)
team2.show_roster()

deck = Deck()
deck.shuffle()
deck.show()

p1.hand.show()
for c in deck.cards:
    p1.hand.add_card(c)

p1.hand.show()

game = Literature(team1, team2)

