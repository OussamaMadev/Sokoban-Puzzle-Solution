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
        current_node = self
        while current_node:
            path.append(current_node.state)
            current_node = current_node.parent
        return path[::-1]  
    def get_solution(self):
        
        solution = []
        current_node = self
        while current_node.parent:
            solution.append(current_node.action)
            current_node = current_node.parent
        return solution[::-1]  