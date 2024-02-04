import pytest
from puzzle import Board, NotReachable, calc_huristic, BoardAStar

world = ("7 2 4 5 b 6 8 3 1")
b = Board(world)

def test_huristic():

   partial_correct = [
       ['1', '2', '3'],
    ['4', '5', '6'],
    ['b', '7', '8']
   ]
   assert calc_huristic(partial_correct) == 2

   partial_correct = [
      ['b', '1', '3'],
    ['4', '2', '5'],
    ['7', '8', '6']
   ]
   assert calc_huristic(partial_correct) == 4

   goal_state = [
       ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', 'b']
   ]
   assert calc_huristic(goal_state) == 0

def test_board_raise_notreachable():
   inversion = "1 2 3 b 4 6 8 5 7"
   with pytest.raises(NotReachable):
      inversion_board = Board(inversion)
   even_inversion = "b 1 3 4 2 5 7 8 6"
   board_good = Board(even_inversion)
   assert board_good.count_inversions() == 4
   
   

# def test_enumerating_action():
#    up_state = [['7', 'b', '4'], ['5', '2', '6'], ['8', '3', '1']]
#    states = b.valid_actions()
#    assert up_state in states

# def test_invalid_actions():
#    right = [
#       ['7', '2', '4'],
#     ['5', '3', '6'],
#     ['8', '1', 'b']
#    ]
#    left = [
#       ['7', '2', '4'],
#     ['5', '3', '6'],
#     ['b', '8', '1']
#    ]
#    no_down = Board("7 2 4 5 3 6 8 b 1")
#    states = no_down.valid_actions()
#    assert len(states) == 3
#    assert right in states
#    assert left in states

#    n_right = Board("2 7 4 5 3 b 8 6 1")
#    states = n_right.valid_actions()
#    assert len(states) == 3

# def test_corner_actions():
#    left_corner = [['2', 'b', '4'], ['5', '3', '7'], ['8', '1', '6']]
#    n_right = Board("b 2 4 5 3 7 8 1 6")
#    states = n_right.valid_actions()
#    assert len(states) == 2
#    assert left_corner in states




if __name__ == "__main__":
   test_huristic()