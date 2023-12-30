import pygame
from enum import Enum
import random as rd

class Oriantation(Enum):
    horizantol = True
    vertical = False

class Grid:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

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
            elif self.grid[coord[1]][coord[0]] == 0:
                self.grid[coord[1]][coord[0]] = 3
                return True
        
        return False

    def ship_at(self, coord: tuple) -> bool:
        x, y = coord
        if self.is_valid_coord(coord):
            if self.grid[y][x] == 1:
                return True
            else:
                return False
        else:
            return False
        
    def is_valid_coord(self, coord: tuple) -> bool:
        x, y = coord
        if 0 <= x < self.size and 0 <= y < self.size:
            return True
        else:
            return False
        
    def display_in_terminal(self):
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
                    if self.grid[i][j] in [1, 2]:  
                        result[i][j] = 1
                elif option == "shots":
                    if self.grid[i][j] in [2, 3]:  
                        result[i][j] = self.grid[i][j]

        return result



class Player:
    def __init__(self):        
        self.grid = Grid()
        self.ships_remaining = [2,2,2,2, 3,3,3, 4,4, 5]
        self.ship_orientation = Oriantation.horizantol
        


    def play_move(self,  enemy: 'Player', game_state):
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
                            if self.shoot_at(enemy, (grid_x, grid_y)):
                                valid_input = True
                                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        self.ship_orientation = Oriantation.vertical
                    elif event.key == pygame.K_h:
                        self.ship_orientation = Oriantation.horizantol


    def shoot_at(self, enemy: 'Player', coord: tuple):
        return enemy.receive_shot(coord)
            


    def receive_shot(self, coord: tuple):
        return self.grid.shoot_at(coord)
         
         

    def place_ship(self, start: tuple, oriantation: 'Oriantation'):
        if self.ships_remaining:
            if self.grid.place_ship(start, self.ships_remaining[0],oriantation.value):
                self.ships_remaining.pop(0)
                return True
            else:
                return False
            
    def is_lost(self) -> bool:
        for row in self.grid.get_grid_elements('all'):
            for cell in row:
                if cell == 1:
                    return False
        
        return True




class BotPlayer(Player):
    def __init__(self):
        super().__init__()
        self.shots_made = set()

    def play_move(self, enemy: Player, game_state):
        valid_input = False
        while not valid_input:
            x = rd.randint(0,9)
            y = rd.randint(0,9)
            

            if game_state == GameState.setup:
                if 0 <= x < 10 and 0 <= y < 10:
                    if self.place_ship((x, y), self.ship_orientation):
                        valid_input = True
            elif game_state == GameState.play:
                if (x,y) not in self.shots_made and 0 <= x < 10 and 0 <= y < 10:
                    if self.shoot_at(enemy, (x, y)):
                        self.shots_made.add((x,y))
                        valid_input = True


class GameState(Enum):
    setup = 1
    play = 2
    game_over = 3



class Turn(Enum):
    player1 = 'player 1'
    player2 = 'player 2'

class BattleShipGame:
    def __init__(self) -> None:
        self.turn = Turn.player1
        self.game_state = GameState.setup
        self.player1 = Player()
        self.player2 = BotPlayer()

        pygame.init()
        self.resolution = (1200,600)
        self.screen = pygame.display.set_mode(self.resolution)  
        pygame.display.set_caption("Battleship")
        #screen.fill((40,108,200))

    def run_game_loop(self, draw: bool):
        if draw:
            self.render()
        while not self.is_game_over():
            self.play_turn()
            self.handle_events()
            self.update_game_state()
            self.is_game_over()
            if draw:
                self.render()

        self.display_winner(self.turn)
        while True:
            self.handle_events()

    def play_turn(self):
        if self.game_state == GameState.setup:
            if self.turn == Turn.player1 :
                self.player1.play_move(self.player2,self.game_state)
            elif self.turn == Turn.player2:
                self.player2.play_move(self.player1,self.game_state)

        elif self.game_state == GameState.play:
            if self.turn == Turn.player1:
                self.player1.play_move(self.player2,self.game_state)
                self.turn = Turn.player2
            else:
                self.player2.play_move(self.player1,self.game_state)
                self.turn = Turn.player1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update_game_state(self):
        if self.game_state == GameState.setup:
            if self.turn == Turn.player1 and not self.player1.ships_remaining:
                self.turn = Turn.player2
            elif self.turn == Turn.player2 and not self.player2.ships_remaining:
                self.game_state = GameState.play
        elif self.game_state == GameState.play:
            if self.player1.is_lost() or self.player2.is_lost():
                self.game_state = GameState.game_over
            
    def render(self):
        self.draw_grid(self.player1.grid.get_grid_elements("all"), 50, (50,50))
        self.draw_grid(self.player2.grid.get_grid_elements("shots"), 50, (600, 50))
        
    def draw_grid(self, grid, cell_size, start_pos):
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                rect = pygame.Rect(start_pos[0] + col_idx * cell_size, start_pos[1] + row_idx * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  
                
                if cell == 1:  # Ship
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                elif cell == 2:  # Hit
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect.left, rect.top), (rect.right, rect.bottom), 3)
                    pygame.draw.line(self.screen, (255, 0, 0), (rect.left, rect.bottom), (rect.right, rect.top), 3)
                elif cell == 3:  # Miss
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, int(cell_size / 4))

            pygame.display.flip()

    def display_winner(self,winner: 'Turn'):
        font = pygame.font.SysFont(None,55)
        if winner == Turn.player1:
            text = font.render("player 1 wins!", True, (255,255,255))
        elif winner == Turn.player2:
            text = font.render("player 1 wins!", True, (255,255,255))

        text_rect = text.get_rect()
        text_rect.center = (self.resolution[0]//2, self.resolution[1]//2)

        background_color = (0, 128, 0) 
        padding = 10 
        background_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(self.screen, background_color, background_rect)
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def is_game_over(self):
        if self.game_state == GameState.game_over:
            return True
        else:
            return False
            


def main():
    game = BattleShipGame()
    game.run_game_loop(True)

if __name__ == "__main__":
    main()