""" AStar.py

A* Search of a problem space.
Partnership? NO
Student Name 1: Alexandre Labbe


UW NetIDs: alabbe
CSE 415, Winter 2024, University of Washington

This code contains my implementation of the A* Search algorithm.

Usage:
python3 AStar.py FranceWithDXHeuristic
"""

import sys
import importlib
from PriorityQueue import My_Priority_Queue


class AStar:
    """
    Class that implements A* Search for any problem space (provided in the required format)
    """
    def __init__(self, problem):
        """ Initializing the AStar class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded.
        self.MAX_OPEN_LENGTH = None  # How long OPEN ever gets.
        self.PATH = None  # List of states from initial to goal, along lowest-cost path.
        self.PATH_LENGTH = None  # Number of states from initial to goal, along lowest-cost path.
        self.TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
        self.BACKLINKS = {}  # Predecessor links, used to recover the path.
        self.OPEN = None  # OPEN list
        self.CLOSED = None  # CLOSED list
        self.VERBOSE = True  # Set to True to see progress; but it slows the search.

        # The value g(s) represents the cost along the best path found so far
        # from the initial state to state s.
        self.g = {}  # We will use a hash table to associate g values with states.
        self.h = None  # Heuristic function

        print("\nWelcome to A*.")

    def runAStar(self):
        # Comment out the line below when this function is implemented.
        """This is an encapsulation of some setup before running
        UCS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        self.h = self.Problem.h
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.ASTAR(initial_state)

        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

    def ASTAR(self, initial_state):
        self.CLOSED = []
        self.BACKLINKS[initial_state] = None

        self.OPEN = My_Priority_Queue()
        # For the start state s0, compute fs and put s0, fs on pq OPEN
        self.OPEN.insert(initial_state, self.h(initial_state))
    
        self.g[initial_state] = 0.0 # do i need this?

        # while open isn't empty 
        while len(self.OPEN) > 0:
            if self.VERBOSE:
                report(self.OPEN, self.CLOSED, self.COUNT)
            if len(self.OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(self.OPEN)

            # find and remove (s,p) with lowest p
            (S, P) = self.OPEN.delete_min()
            # put (s,p) onto closed
            self.CLOSED.append((S, P))

            # if s is a goal state, do goal state stuff
            if self.Problem.GOAL_TEST(S):
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f'Length of solution path found: {self.PATH_LENGTH} edges')
                self.TOTAL_COST = self.g[S]
                print(f'Total cost of solution path found: {self.TOTAL_COST}')
                return
            self.COUNT += 1

            gs = self.g[S] # g cost
            L = [] # empty L list

            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)  # generate list of all s'
                    edge_cost = S.edge_distance(new_state)
                    fs = gs + edge_cost + self.h(new_state) # fs
                    L.append((new_state, fs))
                    updated_priority = True # need to know to change backlinks and edge cost

                    #closed list stuff
                    for (state_c, priority_c) in self.CLOSED:
                        if new_state == state_c: # if state in closed
                            if fs > priority_c:
                                L.remove((new_state, fs))
                                updated_priority = False
                            else:
                                self.CLOSED.remove((state_c, priority_c))
                    
                    #open list stuff
                    if new_state in self.OPEN:
                        q = self.OPEN[new_state]
                        if fs > q:
                            L.remove((new_state, fs))
                            updated_priority = False
                        else:
                            del self.OPEN[new_state]

                    # If the priority was changes, must update backlink and update edge cost
                    if updated_priority:
                        g = S.edge_distance(new_state) + gs
                        self.BACKLINKS[new_state] = S
                        self.g[new_state] = g
                        
                    # add all to open, deleting from open is probably not the most efficient way,
                        # it is to account for updated priority nodes already in open.
                    for (s, q) in L:
                        del self.OPEN[s]
                        self.OPEN.insert(s, q)

        # STEP 6. Go to Step 2.
        return None  # No more states on OPEN, and no goal reached. 

    def backtrace(self, S):
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path   

def print_state_queue(name, q):
    """
    Prints the states in queue q
    """
    print(f"{name} is now: ", end='')
    print(str(q))


def report(opn, closed, count):
    """
    Reports the current statistics:
    Length of open list
    Length of closed list
    Number of states expanded
    """
    print(f"len(OPEN)= {len(opn)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "FranceWithDXHeuristic"
    else:
        Problem = sys.argv[1]
    aStar = AStar(Problem)
    aStar.runAStar()
