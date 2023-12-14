import pygame
import game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))  # Customize as needed
    pygame.display.set_caption("Battleship")
    #screen.fill((40,108,171))

    player1 = game.Player()
    player2 = game.Player()
    player1.place_ship((1,1))
    player1.place_ship((2,1))
    player1.place_ship((3,1))
    player1.place_ship((1,2))
    player2.shoot_at(player1, (2,1))
    player2.place_ship((2,3))
    player1.shoot_at(player2, (2,3))
    player1.shoot_at(player2, (3,3))


    game.display(screen, player1.grid.get_grid_elements("all"))
    game.display(screen, player2.grid.get_grid_elements("shots"), (600, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        

    pygame.quit()

if __name__ == "__main__":
    main()
