import sys
import pygame
import resolvingAlgos
import copy
import queue
from resolvingAlgos import Node
player_pos = (1, 1)
box_positions = [(3, 2)]
target_positions = [(2, 2)]

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

initial_grid = [
    [WALL, WALL,   WALL,   WALL,  WALL,  WALL],
    [WALL, PLAYER,  EMPTY,  EMPTY, EMPTY, WALL],
    [WALL, EMPTY,  TARGET, EMPTY,   EMPTY ,WALL],
    [WALL, EMPTY, BOX,  WALL, EMPTY ,WALL],
    [WALL, EMPTY, EMPTY,    EMPTY, EMPTY ,WALL],
    [WALL, WALL,   WALL,   WALL,  WALL,  WALL],
]

class SokobanPuzzle:
    def __init__(self, grid, player_pos, box_positions, target_positions):
        self.grid = grid
        self.player_pos = player_pos
        self.box_positions = set(box_positions)
        self.target_positions = set(target_positions)

    def isGoal(self):
       return self.box_positions == self.target_positions
    
    def successor_function(self):
        successors = []
        moves = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        for action, (dr, dc) in moves.items():
            new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)

            
            if (0 <= new_player_pos[0] < len(self.grid) and
                    0 <= new_player_pos[1] < len(self.grid[0]) and
                    self.grid[new_player_pos[0]][new_player_pos[1]] != WALL):

                
                new_grid = copy.deepcopy(self.grid)
                new_box_positions = set(self.box_positions) 

                if new_player_pos in self.box_positions: 
                    new_box_pos = (new_player_pos[0] + dr, new_player_pos[1] + dc)

                    
                    if (0 <= new_box_pos[0] < len(self.grid) and
                            0 <= new_box_pos[1] < len(self.grid[0]) and
                            self.grid[new_box_pos[0]][new_box_pos[1]] != WALL and
                            new_box_pos not in self.box_positions):

                       
                        new_box_positions.remove(new_player_pos)
                        new_box_positions.add(new_box_pos)

                        
                        if new_box_pos in self.target_positions:
                            new_grid[new_box_pos[0]][new_box_pos[1]] = BOX_ON_TARGET
                        else:
                            new_grid[new_box_pos[0]][new_box_pos[1]] = BOX

               
                if self.player_pos in self.target_positions:
                    new_grid[self.player_pos[0]][self.player_pos[1]] = TARGET
                else:
                    new_grid[self.player_pos[0]][self.player_pos[1]] = EMPTY

               
                if new_player_pos in self.target_positions:
                    new_grid[new_player_pos[0]][new_player_pos[1]] = PLAYER_ON_TARGET
                else:
                    new_grid[new_player_pos[0]][new_player_pos[1]] = PLAYER

                
                new_state = SokobanPuzzle(new_grid, new_player_pos, new_box_positions, self.target_positions)
                successors.append((action, new_state))

        return successors
    
    def get_boxes(self):
        return self.box_positions
    
    def is_valid_position(self, pos):
        return 0 <= pos[0] < len(self.grid) and 0 <= pos[1] < len(self.grid[0]) and self.grid[pos[0]][pos[1]] != "#"


def animation():

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

state = SokobanPuzzle(initial_grid,player_pos,box_positions,target_positions)

r=resolvingAlgos.BFS(state)

while r.parent :
    resolvingAlgos.printGrid(r.state.grid)
    r=r.parent

resolvingAlgos.printGrid(state.grid)



def a_star(start_state, target_positions, heuristic):
    initNode = Node(start_state)
    initNode.set_f(heuristic, target_positions)
    openList = queue.PriorityQueue()
    openList.put((initNode.f, initNode))
    openListSet = {start_state}
    closedList = set()
    steps = 0  # Count of expanded nodes

    while not openList.empty():
        currentNode = openList.get()
        openListSet.remove(currentNode.state)
        closedList.add(currentNode.state)
        steps += 1

        if currentNode.state.isGoal():
            return currentNode, steps

        for (action, successor) in currentNode.state.successor_function():
            child = Node(successor, currentNode, action, g=currentNode.g + 1)
            if child.state in closedList:
                continue
            child.set_f(heuristic, target_positions)

            if child.state not in openListSet:
                openList.put((child.f, child))
                openListSet.add(child.state)

    return None, steps


# Run the test
def test_a_star(initial_grid, player_pos, box_positions, target_positions):
    initial_state = Node(initial_grid, player_pos, box_positions, target_positions)
    
    print("Testing A* with h1:")
    result_h1, steps_h1 = a_star(initial_state, target_positions, resolvingAlgos.h1(initial_state,target_positions))
    if result_h1:
        print("Solution found with h1 in", steps_h1, "steps.")
        # print("Path to goal with h1:", result_h1.get_solution())
    
    print("\nTesting A* with h2:")
    result_h2, steps_h2 = a_star(initial_state, target_positions, resolvingAlgos.h2(initial_state,target_positions))
    if result_h2:
        print("Solution found with h2 in", steps_h2, "steps.")
        # print("Path to goal with h2:", result_h2.get_solution())


test_a_star(initial_grid, player_pos, box_positions, target_positions)


# animation()
# print('init grid :')
# print(state.player_pos)
# resolvingAlgos.printGrid(state.grid)

# states=state.successor_function()

# print('successor grids :')
# for (action, successor) in states:
#     print(action)
#     print(successor.player_pos)
#     resolvingAlgos.printGrid(successor.grid)
