import numpy as np
import pygame
import time

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Initialize Pygame
pygame.init()


def get_next_generation(grid):
    next_grid = grid.copy()
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            # Count the number of live neighbors
            live_neighbors = np.sum(grid[max(0, row - 1):min(row + 2, rows), max(0, col - 1):min(col + 2, cols)]) - \
                             grid[row, col]

            # Apply the Game of Life rules
            if grid[row, col] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    next_grid[row, col] = 0  # Dies due to underpopulation or overpopulation
            else:
                if live_neighbors == 3:
                    next_grid[row, col] = 1  # A new cell is born due to reproduction
    return next_grid


def update_screen(screen, grid, cell_size):
    screen.fill(WHITE)
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, GRAY, (x, y, cell_size, cell_size), 1)  # Draw grid lines
            if grid[row, col] == 1:
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size))
    pygame.display.flip()


def initialize_scenario(grid, scenario_name):
    grid[:] = 0  # Clear the grid
    if scenario_name == "glider":
        grid[1, 2] = 1
        grid[2, 3] = 1
        grid[3, 1] = 1
        grid[3, 2] = 1
        grid[3, 3] = 1
    elif scenario_name == "blinker":
        grid[2, 1] = 1
        grid[2, 2] = 1
        grid[2, 3] = 1
    elif scenario_name == "toad":
        grid[2, 2] = 1
        grid[2, 3] = 1
        grid[2, 4] = 1
        grid[3, 1] = 1
        grid[3, 2] = 1
        grid[3, 3] = 1
    elif scenario_name == "beacon":
        grid[1, 1] = 1
        grid[1, 2] = 1
        grid[2, 1] = 1
        grid[2, 2] = 1
        grid[3, 3] = 1
        grid[3, 4] = 1
        grid[4, 3] = 1
        grid[4, 4] = 1


def main():
    # Define the grid size
    rows, cols = 20, 40
    cell_size = 20
    grid = np.zeros((rows, cols), dtype=int)  # Start with an empty grid

    # Set up the Pygame screen
    screen_width = cols * cell_size
    screen_height = rows * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game of Life")

    # Initialize a famous scenario
    scenario_name = "beacon"  # Change this to "blinker", "toad", or "beacon" for other scenarios
    initialize_scenario(grid, scenario_name)

    running = True
    clock = pygame.time.Clock()

    # Run the game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid = get_next_generation(grid)
        update_screen(screen, grid, cell_size)
        clock.tick(5)  # Set the frame rate to 5 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
