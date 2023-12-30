from Game import Grid

my_grid = Grid()

my_grid.place_ship((0,0), 5, True)
my_grid.place_ship((0,7), 6, False)

my_grid.shoot_at((0,0))
my_grid.shoot_at((3,0))
my_grid.shoot_at((7,0))

my_grid.shoot_at((12,0))


my_grid.display_in_terminal()

