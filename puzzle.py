import heapq
import copy
WIDTH = 3
HEIGHT = 3

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class BestFirst():
    def __init__(self):
        self.frontier = []
    
    def add(self, node, h_value):
        heapq.heappush(self.frontier, (h_value, node))
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        node = heapq.heappop(self.frontier)
        return node


class Board():
    def __init__(self, world):
        self.world = world
        self.goal_state = [[-1, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.h_value = 0
        self.pos = self.get_position()
    
    def calc_huristic(self):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.world[i][j] != self.goal_state[i][j]:
                    if self.world[i][j] != -1:
                        self.h_value += 1
    
    def get_position(self):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.world[i][j] == -1:
                    return (i,j)

    #given a state, return all possible actions
    def valid_actions(self, state):
        i, j = self.pos
        valid_move = [
            ("up", self.swap((i -1, j))), 
            ("down", self.swap((i + 1, j))),
            ("right", self.swap((i, j+1))),
            ("left", self.swap((i, j-1)))
        ]
        result = []
        for move,state in valid_move:
            if state != None:
                result.append((move, state))
        return result

        
    def swap(self, to_move):
        i, j = to_move
        bi, bj = self.pos
        if 0 <= i <WIDTH and 0 <= j and j<HEIGHT:
            new_state = copy.deepcopy(self.world)
            to_move_value = new_state[i][j]
            new_state[i][j] = -1
            new_state[bi][bj] = to_move_value
            return new_state
        else:
            return None
        




    
    def heuristic_value(self):
        return self.h_value

    def show(self):
        print()
        for row in self.world:
            print(row)
        print()

    





def main():
    world = [[-1, 2, 3], [1, 4, 5], [8, 7, 6]]


if __name__ == "__main__":
    main()