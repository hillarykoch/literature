import literature
from literature.Cards import *
from literature.People import *


ljoker = Card(0, "Little")
ljoker.rng


p1 = Player('Hillary Clinton', 1, 1)
p2 = Player('Zoidberg', 1, 2)
p3 = Player('Meryl Streep', 1, 3)

team = Team('Fungus', 1)

team.show_roster()
team.add_teammate(p1)
team.add_teammate(p2)
team.add_teammate(p3)


deck = Deck()
deck.show()
deck.shuffle()
deck.show()

isinstance(ljoker, Card)
p1.has_card(ljoker)
