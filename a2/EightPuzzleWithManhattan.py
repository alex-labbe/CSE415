"""EightPuzzleWithHamming.py
by Alexandre labbe
UWNetID: alabbe
Student number: 2377032
This file augments EightPuzzle.py with heuristic information,
so that it can be used by an A* implementation.
The particular heuristic is total manhattan distance.
"""

from EightPuzzle import *

goal_state = [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]


def h(s):
    input_array = s.b
    total_distance = 0
    for i in range(3):
        for j in range(3):
            # ignore 0
            if input_array[i][j] != 0:
                for x in range(3):
                    for y in range(3):
                        #find x and y distance from location on goal
                        if goal_state[x][y] == input_array[i][j]:
                            goal_i, goal_j = x, y
                            break
                #sum abs differnce between the two elements, and sum x and y parts
                total_distance += abs(i - goal_i) + abs(j - goal_j)
    return total_distance
#print(h(State([[1,0,2],[3,4,5],[6,7,8]])))