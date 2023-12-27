from Game import Player, Oriantation

player1 = Player()
player2 = Player()

player2.place_ship((1,1), Oriantation.horizantol)

player1.shoot_at(player2, (1,1))



player2.grid.display_in_terminal()

