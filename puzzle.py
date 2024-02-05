#Install python: https://www.python.org/downloads/
#Recommend using vscode to set up python environment: https://code.visualstudio.com/docs/python/python-tutorial
import heapq
import copy
import random
import math

WIDTH = 3
HEIGHT = 3
TRIALS = 5
MAX_STATES = 1000

GOAL_STATE = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "b"]]


class Node:
    def __init__(self, state, parent, h_value, g_value, evaluation):
        self.state = state
        self.h_value = h_value
        self.parent = parent
        self.g = g_value
        self.evaluation = evaluation

    def __lt__(self, other):
        # return self.heuristic_value() < other.heuristic_value()
        return self.evaluation_value() < other.evaluation_value()

    def heuristic_value(self):
        return self.h_value

    def evaluation_value(self):
        return self.evaluation

    def solution(self):
        node = self
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))


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


def find_b(state):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if state[i][j] == "b":
                return (i, j)


# given a state, return all possible actions
def valid_actions(state):
    i, j = find_b(state)
    valid_move = [
        swap((i, j), (i - 1, j), state),
        swap((i, j), (i + 1, j), state),
        swap((i, j), (i, j + 1), state),
        swap((i, j), (i, j - 1), state),
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


def generate_board():
    random_board = ["1", "2", "3", "4", "5", "6", "7", "8", "b"]
    random.shuffle(random_board)
    return random_board


class Board:
    def __init__(self, world):
        self.world_list = world
        self.world = [
            self.world_list[i : i + 3] for i in range(0, len(self.world_list), 3)
        ]
        if self.count_inversions() % 2 != 0:
            raise NotReachable("Cannot reach goal state")
        self.h_value = 0
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

    def calc_huristic(self, world):
        h_value = 0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if world[i][j] != GOAL_STATE[i][j]:
                    if world[i][j] != "b":
                        h_value += 1
        return h_value

    def start(self):
        huristic_state = self.calc_huristic(self.world)
        if huristic_state == 0:
            return
        start = Node(self.world, None, huristic_state, 0, 0)
        frontier = BestFirst()

        frontier.add(start, huristic_state)

        self.explored = set()

        while True:
            node = frontier.remove()
            actions = valid_actions(node.state)

            if node.state == GOAL_STATE:
                steps = 0
                states = node.solution()
                for state in states:
                    print("(", end="")
                    for row in state:
                        for tile in row:
                            print(f"{tile}", end="")
                    print(")-> ", end="")
                    steps += 1
                print(f"Total steps: {steps}")
                return steps
            self.cost += 1
            if self.cost == MAX_STATES:
                print("Too long to calculate")
                return

            state = tuple(tuple(row) for row in node.state)
            self.explored.add(state)

            for state in actions:
                huristic_state = self.calc_huristic(state)
                evaulation = self.calc_evaluation(huristic_state, self.cost)
                state_hash = tuple(tuple(row) for row in state)
                if state_hash not in self.explored:
                    child = Node(state, node, huristic_state, self.cost, evaulation)
                    frontier.add(child, huristic_state)

    def calc_evaluation(self, h_value, g_value):
        return h_value + g_value


class Boardh2(Board):
    def calc_huristic(self, world):
        h_value = 0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if world[i][j] != "b" and world[i][j] != GOAL_STATE[i][j]:
                    for si in range(WIDTH):
                        for sj in range(HEIGHT):
                            if GOAL_STATE[si][sj] == world[i][j]:
                                h_value += abs(i - si) + abs(j - sj)
        return h_value


class Boardh3(Board):
    def calc_huristic(self, world):
        h_value = 0
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if world[i][j] != "b" and world[i][j] != GOAL_STATE[i][j]:
                    for si in range(WIDTH):
                        for sj in range(HEIGHT):
                            if GOAL_STATE[si][sj] == world[i][j]:
                                h_value += math.sqrt((i - si) ** 2 + (j - sj) ** 2)
        return h_value


class BoardAStar(Board):
    def calc_evaluation(self, h_value, g_value):
        return h_value + g_value


class BoardAStarh2(Boardh2):
    def calc_evaluation(self, h_value, g_value):
        return h_value + g_value


class BoardAStarh3(Boardh3):
    def calc_evaluation(self, h_value, g_value):
        return h_value + g_value


def show(world):
    print()
    for row in world:
        print(row)
    print()


def main():
    board = generate_board()
    try:
        bfs = Board(board)
    except NotReachable:
        print("The goal state cannot be reached")
        return
    bfsh2 = Boardh2(board)
    bfsh3 = Boardh3(board)

    astar = BoardAStar(board)
    astarh2 = BoardAStarh2(board)
    astarh3 = BoardAStarh3(board)

    print("GBFS, h1, Tile out of place:")
    bfs.start()
    print("-----------------")
    print("GBFS, h2, Manhattan distance:")
    bfsh2.start()
    print("-----------------")

    print("GBFS, h3, Euclidean Distance")
    bfsh3.start()
    print("-----------------")

    print("Astar h1")
    astar.start()
    print("-----------------")
    print("Astar h2")
    astarh2.start()
    print("-----------------")
    print("Astar h3")
    astarh3.start()
    print("-----------------")


if __name__ == "__main__":
    main()
