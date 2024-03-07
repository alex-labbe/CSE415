"""EightPuzzleWithHamming.py
by Alexandre labbe
UWNetID: alabbe
Student number: 2377032
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is Hamming.
"""


from EightPuzzle import *

goal_state = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]


def h(s):
    input_array = s.b
    
    count = 0
    for i in range(3):
        for j in range(3):
            # if element is not in correct location, count += 1
            if input_array[i][j] != 0:
                if input_array[i][j] != goal_state[i][j]:
                    count += 1
    return count


