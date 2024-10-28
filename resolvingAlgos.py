import queue

class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  
        self.f = 0 
         
    def set_f(self, heuristic, target_positions):
        self.f = self.g + heuristic(self, target_positions)

    def get_path(self):
        path = []
        currentNode = self
        while currentNode:
            path.append(currentNode.state)
            currentNode = currentNode.parent
        return path[::-1]  
    
    def get_solution(self):        
        solution = []
        currentNode = self
        while currentNode.parent:
            solution.append(currentNode.action)
            currentNode = currentNode.parent
        return solution[::-1]  

def printGrid(grid):
    for row in grid:
        print(' '.join(str(cell) for cell in row))
    print("")


def BFS(s):
    initNode = Node(s, None, None)
    openList = queue.Queue(0)
    openListSet = set()  
    closedList = set()   

    if initNode.state.isGoal():
        return initNode

    openList.put(initNode)
    openListSet.add(initNode.state)

    while not openList.empty():
        currentNode = openList.get()
        openListSet.remove(currentNode.state)
        closedList.add(currentNode.state)

        for (action, successor) in currentNode.state.successor_function():
            child = Node(successor, currentNode, action)

            if child.state not in closedList and child.state not in openListSet:
                # printGrid(child.state.grid)
                if child.state.isGoal():
                    return child
                openList.put(child)
                openListSet.add(child.state)

    return None
    
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def h1(node, target_positions):
    nb_left_blocks = sum(1 for box_pos in node.state.get_boxes() if box_pos not in target_positions)
    heuristic_value = 0
    for box_pos in node.state.get_boxes():
        min_distance = min(manhattan_distance(box_pos, target) for target in target_positions)
        heuristic_value += min_distance
    return heuristic_value + nb_left_blocks

def h2(node, target_positions):
    nb_left_blocks = sum(1 for box_pos in node.state.get_boxes() if box_pos not in target_positions)
    heuristic_value = 0
    for box_pos in node.state.get_boxes():
        min_distance = min(manhattan_distance(box_pos, target) for target in target_positions)
        heuristic_value += min_distance
    return 2 * nb_left_blocks + heuristic_value

