import queue

class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  
        self.f = 0  

    def set_f(self, heuristic):
        self.f = self.g + heuristic(self.state)

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

def h1(node):
    nb_left_blocks = sum(1 for box_pos in node.state.box_positions if box_pos not in node.state.target_positions)
    return nb_left_blocks

def h2(node):
    nb_left_blocks = sum(1 for box_pos in node.state.box_positions if box_pos not in node.state.target_positions)
    heuristic_value = 0
    for box_pos in node.state.box_positions:
        if node.state.target_positions:  # Ensure target_positions is not empty
            min_distance = min(manhattan_distance(box_pos, target) for target in node.state.target_positions)
            heuristic_value += min_distance
    return 2 * nb_left_blocks + heuristic_value


def h3(node):
    # nb_left_blocks = h1(node)
    heuristic_value = 0
    for box_pos in node.state.box_positions:
        if node.state.target_positions:  # Ensure target_positions is not empty
            heuristic_value = heuristic_value + manhattan_distance(node.state.player_pos, box_pos)
    return heuristic_value

def getLowestNode(open_set):
    lowestNode = open_set[0]
    for node in open_set:
        if node.f < lowestNode.f:
            lowestNode= node
    
    return lowestNode

# def a_star(start_state, h):
#     open_set = []
#     closed_set = []

#     init_node = Node(start_state)
#     init_node.g = 0
#     init_node.f = h(init_node)  
#     open_set.append(init_node)
    

#     while open_set:
#         current_node = getLowestNode(open_set)
#         open_set.remove(current_node)

#         if current_node.state.isGoal():
#             return current_node

#         closed_set.append(current_node)

#         for action, successor_state in current_node.state.successor_function():
#             child = Node(successor_state, current_node, action)
#             child.g = current_node.g + 1
#             child.f = child.g + h(child)
            
#             if child.state not in [g.state for g in open_set] and child.state not in [g.state for g in closed_set]:
#                 open_set.append(child)

#             else: 
                              
#                 for open in open_set:
#                     if open.state == child.state:
#                         if open.f < child.f:
#                             open_set.remove(open)
#                             open_set.append(child)
                       
                        
#                     else:
#                         for close in closed_set:
#                             if close.state == child.state:
#                                 if close.f < child.f:
#                                     closed_set.remove(close)
#                                     closed_set.append(child)
                                        
#     return None


import heapq


def push_to_open(open, node):
    heapq.heappush(open, (node.f, id(node), node))

def pop_from_open(open):
    _, _, node = heapq.heappop(open)
    return node

def update_open(open, child):
    for i, (f, node_id, existing) in enumerate(open):
        if existing.state == child.state and child.f < f:
            open[i] = (child.f, id(child), child)
            heapq.heapify(open)
            break


def a_star(start_state, h):
    open = []
    closed_set = set()
    init_node = Node(start_state)
    init_node.g = 0
    init_node.f = h(init_node)

    push_to_open(open, init_node)

    while open:
        current_node = pop_from_open(open)

        if current_node.state.isGoal():
            return current_node

        closed_set.add(current_node.state)

        for action, successor_state in current_node.state.successor_function():
            child = Node(successor_state, current_node, action)
            child.g = current_node.g + 1
            child.f = child.g + h(child)

            if child.state not in closed_set:
                in_open = any(existing.state == child.state for _, _, existing in open)

                if not in_open:
                    push_to_open(open, child)
                else:
                    update_open(open, child)

    return None
