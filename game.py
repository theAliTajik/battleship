import pygame
from enum import Enum

class Oriantation(Enum):
    horizantol = True
    vertical = False

class Grid:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        # '~' can represent water, you can use other symbols for ships, hits, and misses

    def place_ship(self, start: tuple, length: int, horizantol: bool) -> bool:
        x, y = start    
        for i in range(length):
            if self.ship_at((x,y)):
               return False
            if horizantol == True:
                x += 1
            else:
                y += 1
        
        x, y = start    
        for i in range(length):
            self.grid[y][x] = 1
            if horizantol == True:
                x += 1
            else:
                y += 1

        return True
                
        
    def shoot_at(self, coord: tuple) -> bool:
        if self.is_valid_coord(coord):
            if self.ship_at(coord):
                self.grid[coord[1]][coord[0]] = 2
                return True
            else:
                self.grid[coord[1]][coord[0]] = 3
                return False
        else:
            return False

    def ship_at(self, coord: tuple) -> bool:
        x, y = coord
        if self.is_valid_coord(coord):
            if self.grid[y][x] == 1:
                return True
            else:
                return False
        else:
            return True
        
    def is_valid_coord(self, coord: tuple) -> bool:
        x, y = coord
        if 0 <= x < self.size and 0 <= y < self.size:
            return True
        else:
            return False
        
    def display_in_terminal(self):
        # Print the grid to the console - for testing
        grid = self.get_grid_elements('all')
        for row in grid:
            print(row)

    def get_grid_elements(self, option):
        if option == "all":
            return self.grid

        result = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if option == "ships":
                    if self.grid[i][j] in [1, 2]:  # Ships and hits shown as ships
                        result[i][j] = 1
                        # Misses and water remain as water
                elif option == "shots":
                    if self.grid[i][j] in [2, 3]:  # Only showing hits and misses
                        result[i][j] = self.grid[i][j]
                        # Ships and water remain hidden

        return result



class Player:
    def __init__(self):        
        self.grid = Grid()
        self.ships_remaining = [2,2,2,2, 3,3,3, 4,4, 5]
        self.ship_orientation = Oriantation.horizantol


    def play_move(self,  enemy: 'Player', game_state):
        #wait for user input
        valid_input = False
        while not valid_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game_state == GameState.setup:
                        x, y = event.pos
                        grid_x = (x - 50) // 50
                        grid_y = (y - 50) // 50
                        if 0 <= grid_x < 10 and 0 <= grid_y < 10:
                            if self.place_ship((grid_x, grid_y), self.ship_orientation):
                                valid_input = True
                    elif game_state == GameState.play:
                        x, y = event.pos
                        grid_x = (x - 600) // 50
                        grid_y = (y - 50) // 50

                        if 0 <= grid_x < 10 and 0 <= grid_y < 10:
                            self.shoot_at(enemy, (grid_x, grid_y))
                            valid_input = True
                                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        self.ship_orientation = Oriantation.vertical
                    elif event.key == pygame.K_h:
                        self.ship_orientation = Oriantation.horizantol


    def shoot_at(self, enemy: 'Player', coord: tuple):
        # Shoot at the specified coordinate of the enemy's grid
        enemy.receive_shot(coord)
            


    def receive_shot(self, coord: tuple):
        if self.grid.shoot_at(coord):
            self.grid.display_in_terminal()
            return True
        else:
            return False

    def place_ship(self, start: tuple, oriantation: 'Oriantation'):
        if self.ships_remaining:
            if self.grid.place_ship(start, self.ships_remaining[0],oriantation.value):
                self.ships_remaining.pop(0)
                return True
            else:
                return False



    # def display_grid(self, option: str):
    #     # Display the player's grid based on the specified option
    #     custom_grid = self.grid.get_grid_elements(option)
    #     self.grid.display_in_terminal(custom_grid)

class GameState(Enum):
    setup = 1
    play = 2
    game_over = 3

class Turn(Enum):
    player1 = 1
    player2 = 2

class BattleShipGame:
    def __init__(self) -> None:
        self.turn = Turn.player1
        self.game_state = GameState.setup
        self.player1 = Player()
        self.player2 = Player()

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))  # Customize as needed
        pygame.display.set_caption("Battleship")
        #screen.fill((40,108,200))

    def run_game_loop(self, draw: bool):
        if draw:
            self.render()
        while not self.is_game_over():
            self.play_turn()
            self.handle_events()
            self.update_game_state()
            if draw:
                self.render()
        pygame.quit()

    def play_turn(self):
        self.player1.play_move(self.player2,self.game_state)

    def handle_events(self):
        ship_orientation_horizontal = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.game_over


    def update_game_state(self):
        if not self.player1.ships_remaining:
            self.game_state = GameState.play


    def render(self):
        self.draw_grid(self.player1.grid.get_grid_elements("all"), 50, (50,50))
        self.draw_grid(self.player2.grid.get_grid_elements("shots"), 50, (600, 50))
        

    def draw_grid(self, grid, cell_size, start_pos):
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                rect = pygame.Rect(start_pos[0] + col_idx * cell_size, start_pos[1] + row_idx * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # Draw cell border
                
                if cell == 1:  # Ship
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                elif cell == 2:  # Hit
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect.left, rect.top), (rect.right, rect.bottom), 3)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect.left, rect.bottom), (rect.right, rect.top), 3)
                elif cell == 3:  # Miss
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, int(cell_size / 4))

            pygame.display.flip()


    def is_game_over(self) -> bool:
        if self.game_state == GameState.game_over:
            return True
        else:
            return False

