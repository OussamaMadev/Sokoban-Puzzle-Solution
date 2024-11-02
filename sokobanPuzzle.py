import sys
import pygame
import resolvingAlgos
import copy
import time

PLAYER = 'R'
BOX = 'B'
WALL = 'O'
TARGET = 'S'
EMPTY = ' '
PLAYER_ON_TARGET = '.'
BOX_ON_TARGET = '*'

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

                if new_player_pos in self.box_positions: # pushing box
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
                
                    else: continue

                if self.player_pos in self.target_positions:
                    new_grid[self.player_pos[0]][self.player_pos[1]] = TARGET
                else:
                    new_grid[self.player_pos[0]][self.player_pos[1]] = EMPTY

                if new_player_pos in self.target_positions:
                    new_grid[new_player_pos[0]][new_player_pos[1]] = PLAYER_ON_TARGET
                else:
                    new_grid[new_player_pos[0]][new_player_pos[1]] = PLAYER

                skipe=False
                for box in box_positions:
                    if box in deadSpots:
                        skipe=True
                        continue
                if not skipe:
                    new_state = SokobanPuzzle(new_grid, new_player_pos, new_box_positions, self.target_positions)
                    successors.append((action, new_state))
            
        return successors
    
    def __eq__(self, other):
        if not isinstance(other, SokobanPuzzle):
            return False
        return (self.player_pos == other.player_pos and
                self.box_positions == other.box_positions and
                self.target_positions == other.target_positions)

    def __hash__(self):
        return hash((self.player_pos, frozenset(self.box_positions), frozenset(self.target_positions)))

def isCorner(pos,grid):
        x,y=pos

        # if on border
        if x==0 or x>=len(grid)-1 or y==0 or y>=len(grid[0])-1 : return False

        if((grid[x+1][y]==WALL and grid[x][y+1]==WALL) 
            or (grid[x+1][y]==WALL and grid[x][y-1]==WALL)
            or (grid[x-1][y]==WALL and grid[x][y+1]==WALL)
            or (grid[x-1][y]==WALL and grid[x][y-1]==WALL)):
            return True
        return False

initial_grid = [
    [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ],
    [ WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
    [ WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, TARGET, BOX, EMPTY, WALL ],
    [ WALL, PLAYER, EMPTY, BOX, WALL, EMPTY, EMPTY, EMPTY, TARGET, WALL ],
    [ WALL, EMPTY, WALL, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL ],
    [ WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, WALL ],
    [ WALL, EMPTY, EMPTY, EMPTY, TARGET, EMPTY, WALL, EMPTY, EMPTY, WALL ],
    [ WALL,  EMPTY,BOX, EMPTY, BOX, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
    [ WALL, EMPTY, EMPTY, EMPTY, EMPTY, TARGET, EMPTY, EMPTY, EMPTY, WALL ],
    [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ]
]

# initial_grid = [
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, PLAYER, EMPTY, BOX, WALL, EMPTY, EMPTY, EMPTY, TARGET, WALL ],
#     [ WALL, EMPTY, WALL, EMPTY, WALL, WALL, WALL, EMPTY, EMPTY, WALL ],
#     [ WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, TARGET, EMPTY, WALL, EMPTY, EMPTY, WALL ],
#     [ WALL,  EMPTY,BOX, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ]
# ]

# initial_grid = [
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL ],
#     [ WALL, EMPTY, PLAYER, EMPTY, EMPTY, TARGET, WALL ],
#     [ WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, WALL ],
#     [ WALL, EMPTY, WALL, BOX, EMPTY, EMPTY, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, WALL ],
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL ]
# ]
# initial_grid = [
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ],
#     [ WALL, EMPTY, EMPTY, WALL, EMPTY, EMPTY, PLAYER, WALL ],
#     [ WALL, EMPTY, WALL, WALL, WALL, WALL, EMPTY, WALL ],
#     [ WALL, EMPTY, EMPTY, BOX, EMPTY, EMPTY, TARGET, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL ],
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ]
# ]

# initial_grid = [
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, WALL, EMPTY, EMPTY, TARGET, WALL ],
#     [ WALL, EMPTY, WALL, EMPTY, WALL, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, PLAYER, EMPTY, BOX, EMPTY, WALL, EMPTY, WALL, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL ]
# ]

# initial_grid = [
#     [ WALL,WALL, WALL,  WALL, WALL, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, TARGET, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY,BOX ,EMPTY  , WALL, WALL ],
#     [ WALL,EMPTY,PLAYER , EMPTY,  EMPTY, WALL ],
#     [ WALL,WALL, WALL, WALL,  WALL, WALL ]
# ]

# initial_grid = [
#     [ WALL,WALL, WALL,  WALL, WALL, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, TARGET, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY, EMPTY, EMPTY, EMPTY, WALL ],
#     [ WALL,EMPTY,BOX ,EMPTY  , WALL, WALL ],
#     [ WALL,EMPTY, EMPTY,PLAYER ,  EMPTY, WALL ],
#     [ WALL,WALL, WALL, WALL,  WALL, WALL ]
# ]

# initial_grid=[
#     [WALL,WALL, WALL,  WALL,WALL, WALL],
#     [WALL,EMPTY, EMPTY,  EMPTY,EMPTY, WALL],
#     [WALL,EMPTY, WALL,  EMPTY,EMPTY, WALL],
#     [WALL,EMPTY, PLAYER,  BOX,EMPTY, WALL],
#     [WALL,EMPTY, BOX,  EMPTY,EMPTY, WALL],
#     [WALL,WALL, WALL,  WALL,WALL, WALL],
# ]


GRID_WIDTH, GRID_HEIGHT = len(initial_grid[0]), len(initial_grid)
box_positions = []
target_positions = []

deadSpots=[]

for i in range(GRID_HEIGHT):
    for  j in range(GRID_WIDTH):
        elem=initial_grid[i][j]
        if ( elem == PLAYER or elem == PLAYER_ON_TARGET):
            player_pos = (i, j)
        if (elem == BOX or elem == BOX_ON_TARGET):
            box_positions.append((i, j))
        if (elem == TARGET or elem == PLAYER_ON_TARGET or elem == BOX_ON_TARGET):
            target_positions.append((i, j))
        if (isCorner((i,j),initial_grid)):
            deadSpots.append((i,j)) 

# @todo complete the daedrSpots recognition 

print(target_positions)
print(box_positions)
TILE_SIZE = 50
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_img = pygame.transform.scale(pygame.image.load('./Sokoban-Puzzle-Solution/imgs/angry-birds.png'), (TILE_SIZE, TILE_SIZE)) 
wall_img = pygame.transform.scale(pygame.image.load('./Sokoban-Puzzle-Solution/imgs/wall.png') , (TILE_SIZE, TILE_SIZE)) 
box_img = pygame.transform.scale(pygame.image.load('./Sokoban-Puzzle-Solution/imgs/box.png'), (TILE_SIZE, TILE_SIZE)) 
target_img = pygame.transform.scale(pygame.image.load('./Sokoban-Puzzle-Solution/imgs/target.png') , (TILE_SIZE, TILE_SIZE)) 
empty_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
empty_img.fill(WHITE) 

def draw_grid(grid,screen):
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

def draw_text(screen, text, x, y, font_size=30, color=(0, 0, 0), bg_color=(0, 0, 0, 150)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
    bg_surface.fill(bg_color)
    screen.blit(bg_surface, bg_surface.get_rect(center=text_rect.center))
    screen.blit(text_surface, text_rect)

def animation(nodes,delay):

    pygame.init()
    pygame.display.set_caption("Sokoban Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    i=0
    nodes.reverse()
    end=len(nodes)-1
    running = True
    while running:  
        screen.fill(WHITE)
        
        if(i<end+1):
            draw_grid(nodes[i],screen)
            i=i+1
        else:
            draw_grid(nodes[end],screen)
            if end>0:
                draw_text(screen, "DONE", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, font_size=100, color=(0, 255, 0), bg_color=(0, 0, 0, 150))
            else :
                draw_text(screen, "the game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, font_size=100, color=(0, 255, 0), bg_color=(0, 0, 0, 50))
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        time.sleep(delay)

    pygame.quit()

state = SokobanPuzzle(initial_grid,player_pos,box_positions,target_positions)

animation([initial_grid],0.5)
t=time.time()
r=resolvingAlgos.BFS(state)
print(time.time()-t)
if (not r):
    print('not possible to solve')
    exit()

grids=[r.state.grid]

while r.parent :
    # resolvingAlgos.printGrid(r.state.grid)
    r=r.parent
    grids.append(r.state.grid)

animation(grids,0.6)
