from itertools import product
import copy

coord_grid = list(product(range(3), range(3)))

# Coordinate system
#    x
#    0 1 2
# y 0
#   1
#   2

goal_state = [
    [1, 2, 3],
    [8, None, 4],
    [7, 6, 5]
]

initial_state_3a = [
    [2, 3, None],
    [1, 8, 4],
    [7, 6, 5]
]

initial_state_3b = [
    [2, 3, None],
    [1, 7, 4],
    [8, 6, 5]
]


def print_state(s, name):
    print(name)
    pretty_s = ''
    for y in range(3):
        for x in range(3):
            if s[y][x]:
                pretty_s += str(s[y][x])
            else:
                pretty_s += "X"
            pretty_s += " "
        pretty_s += "\n"
    print(pretty_s)


def f(s):
    mismatched_tiles = 0
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] and s[i][j] != goal_state[i][j]:
                mismatched_tiles += 1
    return mismatched_tiles

# Returns the coordinate of the empty piece
def find_empty_coord(s):
    for y, x in coord_grid:
        if s[y][x] == None:
            return (x, y)


# UP, DOWN, LEFT, RIGHT
# Calculate the new coord of the empty piece after transition
transition_coord_fns = [
    lambda x, y: (x, y-1),
    lambda x, y: (x, y+1),
    lambda x, y: (x-1, y),
    lambda x, y: (x+1, y)
]

# Returns the 4 possible successor states in this sequence, UP, DOWN, LEFT, RIGHT
# If the successor states are invalid, return None.
def transition_fn(s):
    successor_states = []
    empty_coord = find_empty_coord(s)
    for transition_coord_fn in transition_coord_fns:
        successor_empty_coord = transition_coord_fn(*empty_coord)
        if all([0 <= c and c <= 2 for c in successor_empty_coord]):
            successor_s = copy.deepcopy(s)
            cx, cy = empty_coord
            sx, sy = successor_empty_coord
            successor_s[cy][cx] = s[sy][sx]
            successor_s[sy][sx] = None
            successor_states.append(successor_s)
        else:
            successor_states.append(None)
    return successor_states


# Check your impl so far
# print(f"f(inital_3a) = {f(inital_state_3a)}")
seq_names = ["UP", "DOWN", "LEFT", "RIGHT"]
# for succ_s, seq_name in zip(transition_fn(inital_state_3a), seq_names):
#     if succ_s:
#         print_state(succ_s, f"inital_3a, {seq_name}, f={f(succ_s)}")

# Print the trace, like below.
'''
========== Hill Climbing 3a ==========
DOWN, f=5
2 3 4 
1 8 X 
7 6 5 

LEFT, f=3
2 X 3 
1 8 4 
7 6 5 

--------------------
'''

# Now we solve 3a using code
def hill_climbing(inital_state):
    curr = inital_state
    while True:
        terminate = True
        seq = None
        succs = transition_fn(curr)
        for i in range(len(succs)):
            if succs[i]:
                if f(succs[i]) < f(curr):
                    seq = i
                    curr = succs[i]
                    terminate = False
        if terminate:
            break
        else:
            print_state(curr, f"{seq_names[seq]}, f={f(curr)}")
    return curr


print_state(goal_state, "goal_state")

print("========== Hill Climbing 3a ==========")
print_state(initial_state_3a, "initial_state_3a")
minima_state = hill_climbing(initial_state_3a)
print_state(minima_state, f"minima_state 3a, f={f(minima_state)}")

print("========== Hill Climbing 3b ==========")
print_state(initial_state_3b, "initial_state_3b")
minima_state = hill_climbing(initial_state_3b)
print_state(minima_state, f"minima_state 3b, f={f(minima_state)}")
