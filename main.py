import pygame
import game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))  # Customize as needed
    pygame.display.set_caption("Battleship")
    #screen.fill((40,108,200))

    ship_orientation_horizontal = True

    player1 = game.Player()
    player2 = game.Player()


    
    game.display(screen, player2.grid.get_grid_elements("shots"), (600, 50))

    running = True
    while running:
        game.display(screen, player1.grid.get_grid_elements("all"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_state == "setup":
                    x, y = event.pos
                    grid_x = (x - 50) // 50
                    grid_y = (y - 50) // 50
                    if 0 <= grid_x < 10 and 0 <= grid_y < 10:
                        player1.place_ship((grid_x, grid_y), ship_orientation_horizontal)        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    ship_orientation_horizontal = False
                elif event.key == pygame.K_h:
                    ship_orientation_horizontal = True
        
        

    pygame.quit()

if __name__ == "__main__":
    main()
