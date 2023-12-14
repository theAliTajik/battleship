import pygame

current_player = None

class Grid:
    def __init__(self, size=10):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]
        # '~' can represent water, you can use other symbols for ships, hits, and misses

    def place_ship(self, coordinate:tuple):
        self.grid[coordinate[1]][coordinate[0]] = "#"
        

    def is_valid_placement(self, start, end):
        # Check if the placement of the ship is valid
        # Implement checks for ship overlapping and out-of-bounds placement
        pass

    def shoot_at(self, coord):
        if self.is_ship_hit(coord):
            self.grid[coord[1]][coord[0]] = "X"
            return True
        else:
            self.grid[coord[1]][coord[0]] = "O"
            return False
        # Record a shot at the given coordinate
        # Update the grid based on whether it's a hit or miss
        

    def is_ship_hit(self, coord) -> bool:
        if self.grid[coord[1]][coord[0]] == "#":
            return True
        else:
            return False
        # Determine if a ship is hit at the given coordinate

    def display(self, grid):
        # Print the grid to the console - for testing
        for row in grid:
            print(" ".join(row))
        print()
    
    def get_grid_elements(self, option):
        """
        Return specific elements of the grid based on the option:
        - "ships": Only the ships, turning hits into ships and misses into water
        - "shots": Only the hits and misses, hiding the ships
        - "all": Both ships and hits and misses
        """
        if option == "all":
            return self.grid

        result = [["~" for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if option == "ships":
                    if self.grid[i][j] in ["#", "X"]:  # Ships and hits shown as ships
                        result[i][j] = "#"
                    # Misses and water remain as water
                elif option == "shots":
                    if self.grid[i][j] in ["X", "O"]:  # Only showing hits and misses
                        result[i][j] = self.grid[i][j]
                    # Ships and water remain hidden

        return result
    


    # You can add more methods as needed, such as checking for game over conditions,
    # or methods to support AI decision-making

class Player:
    def __init__(self):
        self.grid = Grid()

    def shoot_at(self, enemy: 'Player', coord: tuple):
        # Shoot at the specified coordinate of the enemy's grid
        if enemy.receive_shot(coord):
            print("Hit!")
        else:
            print("miss")

    def receive_shot(self, coord: tuple):
        # Handle a shot at the player's grid
        return self.grid.shoot_at(coord)

    def place_ship(self, coordinates: tuple):
        # Place a ship at the specified coordinates on the player's grid
        self.grid.place_ship(coordinates)

    def display_grid(self, option: str):
        # Display the player's grid based on the specified option
        custom_grid = self.grid.get_grid_elements(option)
        self.grid.display(custom_grid)

def update():
    # Update game state
    pass

def draw_grid(screen, grid, cell_size, start_pos):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            rect = pygame.Rect(start_pos[0] + col * cell_size, start_pos[1] + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Draw cell border
            cell = grid[row][col]
            if cell == "#":  # Ship
                pygame.draw.rect(screen, (128, 128, 128), rect)
            elif cell == "X":  # Hit
                pygame.draw.rect(screen, (128, 128, 128), rect)
                pygame.draw.line(screen, (255, 0, 0), (rect.left, rect.top), (rect.right, rect.bottom), 3)
                pygame.draw.line(screen, (255, 0, 0), (rect.left, rect.bottom), (rect.right, rect.top), 3)
            elif cell == "O":  # Miss
                pygame.draw.circle(screen, (0, 0, 255), rect.center, int(cell_size / 4))

def display(screen, grid,  start_pos=(50,50)):
    cell_size = 50
    
    draw_grid(screen, grid, cell_size, start_pos)

    pygame.display.flip()

