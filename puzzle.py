import heapq
import copy

WIDTH = 3
HEIGHT = 3

GOAL_STATE = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "b"]]

class Node:
    def __init__(self, state, parent, h_value):
        self.state = state
        self.h_value = h_value
        self.parent = parent

    def __lt__(self, other):
        return self.heuristic_value() < other.heuristic_value()

    def heuristic_value(self):
        return self.h_value


class BestFirst:
    def __init__(self):
        self.frontier = []

    def add(self, node, h_value):
        heapq.heappush(self.frontier, (h_value, node))

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        node = heapq.heappop(self.frontier)
        return node[1]


class NotReachable(Exception):
    pass

def calc_huristic(world):
        h_value = 0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if world[i][j] != GOAL_STATE[i][j]:
                    if world[i][j] != "b":
                        h_value += 1
        return h_value
def find_b(state):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if state[i][j] == 'b':
                return (i, j)

# given a state, return all possible actions
def valid_actions(state):
    i, j= find_b(state)
    valid_move = [
        swap((i,j), (i - 1, j), state),
        swap((i,j), (i + 1, j), state),
        swap((i,j), (i, j + 1), state),
        swap((i,j), (i, j - 1), state),
    ]
    result = []
    for state in valid_move:
        if state != None:
            result.append((state))
    return result

def swap(bpos, to_move, world):
    i, j = to_move
    bi, bj = bpos
    if 0 <= i < WIDTH and 0 <= j and j < HEIGHT:
        new_state = copy.deepcopy(world)
        to_move_value = new_state[i][j]
        new_state[i][j] = "b"
        new_state[bi][bj] = to_move_value
        return new_state
    else:
        return None

class Board:
    def __init__(self, world):
        self.world_list = self.make_list(world)
        self.world = [
            self.world_list[i : i + 3] for i in range(0, len(self.world_list), 3)
        ]
        if self.count_inversions() % 2 != 0:
            raise NotReachable("Cannot reach goal state")
        self.h_value = 0
        self.pos = self.get_position()
        self.cost = 0

    def make_list(self, world):
        result = [
            char if char.isdigit() else "b" if char == "b" else char
            for char in world.split()
        ]
        return result

    def count_inversions(self):
        inversions = 0
        current = 0
        n = WIDTH * HEIGHT
        for i in range(n - 1):
            for j in range(i + 1, n):
                current = self.world_list[i]
                index = self.world_list[j]
                if current != "b" and index != "b":
                    if int(current) > int(index):
                        inversions += 1

        return inversions

    def get_position(self):
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.world[i][j] == "b":
                    return (i, j)

    

    def start(self):
        huristic_state = calc_huristic(self.world)
        if huristic_state == 0:
            return
        start = Node(self.world, None, huristic_state)
        frontier = BestFirst()

        frontier.add(start, huristic_state)

        self.explored = set()

        while True:
            node = frontier.remove()
            actions = valid_actions(node.state)

            if node.state == GOAL_STATE:
                print("Done")
                show(node.state)
                print(self.cost)
                return
            self.cost += 1

            state = tuple(tuple(row) for row in node.state)
            self.explored.add(state)

            for state in actions:
                huristic_state = calc_huristic(state)
                state_hash = tuple(tuple(row) for row in state)
                if state_hash not in self.explored:
                    child = Node(state, node, huristic_state)
                    frontier.add(child, huristic_state)


def show(world):
    print()
    for row in world:
        print(row)
    print()


def main():
    world = "b 1 3 4 2 5 7 8 6"
    b = Board(world)
    b.start()


if __name__ == "__main__":
    main()
