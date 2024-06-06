import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Define the shapes of the tetrominos
tetrominos = [
    [[1, 1, 1],
     [0, 1, 0]],  # T
    [[0, 2, 2],
     [2, 2, 0]],  # S
    [[3, 3, 0],
     [0, 3, 3]],  # Z
    [[4, 4],
     [4, 4]],  # O
    [[5, 5, 5, 5]],  # I
    [[0, 0, 6],
     [6, 6, 6]],  # J
    [[7, 0, 0],
     [7, 7, 7]],  # L
]

# Define the size of the grid and the size of each cell
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Define the width and height of the screen
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to create a new tetromino
def new_tetromino():
    tetromino = random.choice(tetrominos)
    color = random.choice([RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW])
    x = GRID_WIDTH // 2 - len(tetromino[0]) // 2
    y = 0
    return {"shape": tetromino, "color": color, "x": x, "y": y}

# Function to draw the tetromino on the screen
def draw_tetromino(tetromino, dx=0, dy=0):
    for y, row in enumerate(tetromino["shape"]):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino["color"], pygame.Rect((tetromino["x"] + x + dx) * CELL_SIZE, (tetromino["y"] + y + dy) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

# Function to check if a tetromino is colliding with the grid or another tetromino
def is_collision(tetromino, dx=0, dy=0):
    for y, row in enumerate(tetromino["shape"]):
        for x, cell in enumerate(row):
            if cell:
                if tetromino["x"] + x + dx < 0 or tetromino["x"] + x + dx >= GRID_WIDTH or tetromino["y"] + y + dy >= GRID_HEIGHT:
                    return True
                if grid[tetromino["y"] + y + dy][tetromino["x"] + x + dx]:
                    return True
    return False

# Function to draw the grid
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, GRAY, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Function to draw the current state of the game
def draw(score):
    screen.fill(BLACK)
    draw_grid()
    draw_tetromino(current_tetromino)
    for tetromino in fallen_tetrominos:
        draw_tetromino(tetromino)
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

# Function to update the grid with the fallen tetrominos
def update_grid():
    for tetromino in fallen_tetrominos:
        for y, row in enumerate(tetromino["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    grid[tetromino["y"] + y][tetromino["x"] + x] = 1

# Function to remove completed rows from the grid
def remove_completed_rows():
    global score
    rows_removed = 0
    y = GRID_HEIGHT - 1
    while y >= 0:
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0] * GRID_WIDTH)
            rows_removed += 1
        else:
            y -= 1
    score += rows_removed ** 2

# Function to handle user input
def handle_input():
    global current_tetromino
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not is_collision(current_tetromino, dx=-1):
                current_tetromino["x"] -= 1
            if event.key == pygame.K_RIGHT and not is_collision(current_tetromino, dx=1):
                current_tetromino["x"] += 1
            if event.key == pygame.K_DOWN and not is_collision(current_tetromino, dy=1):
                current_tetromino["y"] += 1
            if event.key == pygame.K_UP:
                rotated_tetromino = {"shape": [[current_tetromino["shape"][j][i] for j in range(len(current_tetromino["shape"]))] for i in range(len(current_tetromino["shape"][0]))], "color": current_tetromino["color"], "x": current_tetromino["x"], "y": current_tetromino["y"]}
                if not is_collision(rotated_tetromino):
                    current_tetromino["shape"] = rotated_tetromino["shape"]

# Function to update the game state
def update():
    global current_tetromino
    if is_collision(current_tetromino, dy=1):
        fallen_tetrominos.append(current_tetromino)
        current_tetromino = new_tetromino()
        update_grid()
        remove_completed_rows()
        if is_collision(current_tetromino):
            game_over()
    else:
        current_tetromino["y"] += 1

# Function to handle game over
def game_over():
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25))
    pygame.display.flip()
    pygame.time.delay(2000)  # Display "GAME OVER" for 2 seconds
    pygame.quit()
    exit()

# Initialize the game state
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
current_tetromino = new_tetromino()
fallen_tetrominos = []
score = 0

# Main game loop
while True:
    handle_input()
    update()
    draw(score)
    clock.tick(5)
