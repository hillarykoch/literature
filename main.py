import literature
from literature.Card import Card
from literature.People import *


joker = Card(0, "Little")
joker.rng


p1 = Player('Hillary Clinton', 1, 1)
p2 = Player('Zoidberg', 1, 2)
p3 = Player('Meryl Streep', 1, 2)

team = Team('Fungus', 1)

team.show_roster()
team.add_teammate(p1)
team.add_teammate(p2)
team.show_roster()
team.add_teammate(p3)
p3.change_player_number(3)

p3.player_number
p3.position
team.show_roster()
team.add_teammate(p3)
team.show_roster()



