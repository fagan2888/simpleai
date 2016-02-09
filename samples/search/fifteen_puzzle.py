'''
15 puzzle problem

States are defined as string representations of the pieces on the puzzle.
Actions denote what piece will be moved to the empty space.

States must always be immutable. We will use strings, but internally most of
the time we will convert those strings to lists, which are easier to handle.
For example, the state (string):

'1-2-3-4
 5-6-7-8
 9-10-11-12
 13-14-15-e'

will become (in lists):

[['1', '2', '3', '4'],
 ['5', '6', '7', '8'],
 ['9', '10', '11','12],
 ['13','14','15','e']]

'''
import sys
sys.path.append('../../../simpleai') # if you didn't install simpleai package, just clone the repo and append it to the path
from simpleai.search import astar, uniform_cost, depth_first, limited_depth_first, breadth_first, iterative_limited_depth_first


GOAL = '''1-2-3-4
5-6-7-8
9-10-11-12
13-14-15-e'''

## easy ###
INITIAL = '''1-e-2-4
5-7-3-8
9-6-11-12
13-10-14-15'''

### Case 1 ###
# INITIAL = '''11-5-12-14
# 15-2-e-9
# 13-7-6-1
# 3-10-4-8'''


# # ### Case 2 ###
# INITIAL = '''13-5-8-3
# 7-1-9-4
# 14-10-6-15
# 2-12-11-e'''


def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])


def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]


def find_location(rows, element_to_find):
    '''Find the location of a piece in the puzzle.
       Returns a tuple: row, column'''
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic


# we create a cache for the goal position of each piece, so we don't have to
# recalculate them every time
goal_positions = {}
rows_goal = string_to_list(GOAL)

# for 15 nums
nums = [str(i) for i in range(1, 16)]
nums.append('e')

for number in nums:
    goal_positions[number] = find_location(rows_goal, number)


class FifteenPuzzleProblem():

    def __init__(self, initial_state=None):
        self.initial_state = initial_state

    def actions(self, state):
        '''Returns a list of the pieces we can move to the empty space.'''
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')

        actions = []
        if row_e > 0:
            actions.append(rows[row_e - 1][col_e])
        if row_e < 3:
            actions.append(rows[row_e + 1][col_e])
        if col_e > 0:
            actions.append(rows[row_e][col_e - 1])
        if col_e < 3:
            actions.append(rows[row_e][col_e + 1])

        return actions

    def result(self, state, action):
        '''Return the resulting state after moving a piece to the empty space.
           (the "action" parameter contains the piece to move)
        '''
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')
        row_n, col_n = find_location(rows, action)

        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]

        return list_to_string(rows)

    def is_goal(self, state):
        '''Returns true if a state is the goal state.'''
        return state == GOAL

    def cost(self, state1, action, state2):
        '''Returns the cost of performing an action. No useful on this problem, i
           but needed.
        '''
        return 1

    def heuristic(self, state):
        '''Returns an *estimation* of the distance from a state to the goal.
           We are using the manhattan distance.
        '''
        rows = string_to_list(state)

        distance = 0

        # for 15 nums
        # nums = [str(i) for i in range(1, 16)]
        # nums.append('e')

        for number in nums:
            row_n, col_n = find_location(rows, number)
            print(find_location(rows, number))
            row_n_goal, col_n_goal = goal_positions[number]

            distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)

        return distance



def main():

    # to record running time
    import time
    start = time.time()
    #### Uncomment an algorithm to use ####
    # result = depth_first(FifteenPuzzleProblem(INITIAL), 1)
    result = breadth_first(FifteenPuzzleProblem(INITIAL), 1)
    # result = limited_depth_first(FifteenPuzzleProblem(INITIAL), depth_limit=8)
    # result = iterative_limited_depth_first(FifteenPuzzleProblem(INITIAL),1)
    end = time.time()


    def report_result(result):
        count = 1
        for action, state in result.path():
            print("**** STEP NUMBER: {} ****".format(count))
            count += 1
            print('Move number', action)
            print(state)

        # Running time
        print("\ntime taken: ", end - start)

    report_result(result)

    # visualize the solution using pygraph module, to use pygraph see: http://github.com/iamaziz/pygraph

    try:
        from pygraph.dgraph import PyGraph
    except ImportError:
        pass

    name = 'easy-BFS'

    def vizit(name):

        g = PyGraph()
        for i in range(len(result.path())):
            try:
                a1, s1 = result.path()[i]
                a2, s2 = result.path()[i+1]
                r = [s1, a2, s2]
                relation = ' '.join(r)
                g.add_relation(relation)
            except IndexError:
                pass

        g.draw_graph("15-puzzle-{}".format(name), orientation="LR")

    # vizit(name)

if __name__ == '__main__':
    main()
