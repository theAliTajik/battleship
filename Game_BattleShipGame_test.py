from Game import Grid, BattleShipGame



my_game = BattleShipGame()
my_grid = Grid()

my_grid.place_ship((3,5), 5, True)
my_grid.place_ship((3,7), 5, True)

my_grid.place_ship((0,0), 5, True)
my_grid.place_ship((0,2), 6, False)

my_grid.shoot_at((0,0))
my_grid.shoot_at((3,0))
my_grid.shoot_at((7,0))

my_game.draw_grid(my_grid.get_grid_elements('all'), 50, (50,50))

my_game.run_game_loop(False)