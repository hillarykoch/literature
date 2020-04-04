import literature
from literature.Cards import *
from literature.People import *


ljoker = Card(0, "Little")
ljoker.rng


p1 = Player('Hillary Clinton', 1, 1)
p2 = Player('Zoidberg', 2, 2)
p3 = Player('Meryl Streep', 1, 3)

team = Team('Fungus', 1)
team2 = Team('Marge', 2)

team.show_roster()
team.add_teammate(p1)
team2.add_teammate(p2)
team.add_teammate(p3)


deck = Deck()
deck.show()
deck.shuffle()
deck.show()

p1.add_card(ljoker)
p1.add_card(Card(5, "spades"))
p1.add_card(Card(13, "hearts"))
p1.has_card(ljoker)
p1.has_card(Card(7,"clubs"))

p2.add_card(Card(4, "spades"))
p2.ask_for_card(p1, Card(5, "spades"))
p2.hand