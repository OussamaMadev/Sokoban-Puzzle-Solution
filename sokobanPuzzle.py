import sys
import pygame

class SokobanPuzzle:
    def __init__(self, grid, player_pos, box_positions, target_positions):
        self.grid = grid
        self.player_pos = player_pos
        self.box_positions = set(box_positions)
        self.target_positions = set(target_positions)

    def is_goal(self):
       return self.box_positions == self.target_positions

    def successor_function(self):
        successors = []
        moves = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        
        for action, (dr, dc) in moves.items():
            new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
            
            # If the player moves into a wall, skip this move
            if self.grid[new_player_pos[0]][new_player_pos[1]] == 'O':
                continue
            
            # Check if there's a box at the new position
            if new_player_pos in self.box_positions:
                # Calculate the position where the box would be pushed
                new_box_pos = (new_player_pos[0] + dr, new_player_pos[1] + dc)
                
                # Ensure the box isn't pushed into a wall or another box
                if self.grid[new_box_pos[0]][new_box_pos[1]] != 'O' and new_box_pos not in self.box_positions:
                    # Create a new state with the box moved
                    new_box_positions = self.box_positions.copy()
                    new_box_positions.remove(new_player_pos)
                    new_box_positions.add(new_box_pos)
                    new_state = SokobanPuzzle(self.grid, new_player_pos, new_box_positions, self.target_positions)
                    successors.append((action, new_state))
            else:
                # No box in the way, just move the player
                new_state = SokobanPuzzle(self.grid, new_player_pos, self.box_positions, self.target_positions)
                successors.append((action, new_state))
        
        return successors

TILE_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 6, 6
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER = 'R'
BOX = 'B'
WALL = 'O'
TARGET = 'S'
EMPTY = ' '
PLAYER_ON_TARGET = '.'
BOX_ON_TARGET = '*'

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban Game")

player_img = pygame.image.load('./imgs/angry-birds.png') 
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE)) 

wall_img = pygame.image.load('./imgs/wall.png') 
wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE)) 

box_img = pygame.image.load('./imgs/box.png') 
box_img = pygame.transform.scale(box_img, (TILE_SIZE, TILE_SIZE)) 

target_img = pygame.image.load('./imgs/target.png') 
target_img = pygame.transform.scale(target_img, (TILE_SIZE, TILE_SIZE)) 

empty_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
empty_img.fill(WHITE) 


initial_grid = [
    [WALL, WALL,   WALL,   WALL,  WALL,  EMPTY],
    [WALL, EMPTY,  EMPTY,  EMPTY, WALL, WALL],
    [WALL, EMPTY,  TARGET, BOX,   EMPTY ,WALL],
    [WALL, PLAYER, EMPTY,  WALL, EMPTY ,WALL],
    [WALL, EMPTY,  EMPTY,  EMPTY, EMPTY ,WALL],
    [WALL, WALL,   WALL,   WALL,  WALL,  WALL],
]

player_pos = (3, 1)
box_positions = [(1, 3)]
target_positions = [(2, 2)]


def draw_grid(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            element = grid[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if element == PLAYER:
                screen.blit(player_img, (x, y))
            elif element == BOX:
                screen.blit(box_img, (x, y))
            elif element == WALL:
                screen.blit(wall_img, (x, y))
            elif element == TARGET:
                screen.blit(target_img, (x, y))
            elif element == EMPTY:
                screen.blit(empty_img, (x, y))
            elif element == PLAYER_ON_TARGET:
                screen.blit(player_img, (x, y))  
            elif element == BOX_ON_TARGET:
                screen.blit(box_img, (x, y)) 


def move_player(grid, direction):
    global player_pos
    row, col = player_pos
    dr, dc = direction
    new_row, new_col = row + dr, col + dc

    if grid[new_row][new_col] in [EMPTY, TARGET]: 
        if grid[row][col] == PLAYER_ON_TARGET:
            grid[row][col] = TARGET 
        else:
            grid[row][col] = EMPTY

        player_pos = (new_row, new_col)

        if grid[new_row][new_col] == TARGET:
            grid[new_row][new_col] = PLAYER_ON_TARGET
        else:
            grid[new_row][new_col] = PLAYER
    elif grid[new_row][new_col] in [BOX, BOX_ON_TARGET]:  
        box_new_row, box_new_col = new_row + dr, new_col + dc
        if grid[box_new_row][box_new_col] in [EMPTY, TARGET]:  
            if grid[box_new_row][box_new_col] == TARGET:
                grid[box_new_row][box_new_col] = BOX_ON_TARGET
            else:
                grid[box_new_row][box_new_col] = BOX

            if grid[new_row][new_col] == BOX_ON_TARGET:
                grid[new_row][new_col] = PLAYER_ON_TARGET
            else:
                grid[new_row][new_col] = PLAYER

            if grid[row][col] == PLAYER_ON_TARGET:
                grid[row][col] = TARGET
            else:
                grid[row][col] = EMPTY

            player_pos = (new_row, new_col)


def check_win(grid):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] == BOX:
                return False
    return True

running = True
while running:
    screen.fill(WHITE)

    draw_grid(initial_grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(initial_grid, (-1, 0))
            elif event.key == pygame.K_DOWN:
                move_player(initial_grid, (1, 0))
            elif event.key == pygame.K_LEFT:
                move_player(initial_grid, (0, -1))
            elif event.key == pygame.K_RIGHT:
                move_player(initial_grid, (0, 1))

    if check_win(initial_grid):
        print("You won!")
        running = False

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()

