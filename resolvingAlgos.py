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
    

# Function BFS (s, successorsFn, isGoal)
# Begin
# Open: queue /* FIFO list */
# Closed: list
# init_node <- Node (s, None, None) /* A data structure with (state, parentNode, action) attributes*/

# if (isGoal(init_node.state)) then return init_node
# Open.enqueue(init_node)
# Closed <- [ ]

# while (not Open.empty()) do
#   current <- Open.dequeue() /* Choose the shallowest node in Open */
#   Closed.add(current)
#   for each (action, successor) in successorsFn(current.state) do
#       child <- Node (successor, current, action) /* Create a new node and link it to its parent */
#       if (child.state not in Closed and not in Open) then
#           if (isGoal(child.state)) then return child
#           Open.enqueue(child)

# return None
# End
