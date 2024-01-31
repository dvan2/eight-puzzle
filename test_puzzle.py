from puzzle import Board

world = [
        [7,2,4],
        [5,-1,6],
        [8,3,1]
   ] 
b = Board(world)

def test_huristic():
   b.calc_huristic()
   assert b.heuristic_value() == 8

def test_enumerating_action():
   up_state = [
        [7,-1,4],
        [5,2,6],
        [8,3,1]
   ] 
   actions_states = b.valid_actions(world)
   actions = [action[0] for action in actions_states]
   states = [state[1] for state in actions_states]

   assert "up" in actions
   assert up_state in states

if __name__ == "__main__":
   test_enumerating_action()