'''Farmer_Fox.py
by Alexandre Labbe
UWNetIDs: alabbe
Student numbers: 2377032

Assignment 2, in CSE 415, Winter 2024
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
SOLUTION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "06-APR-2021"
#</METADATA>


#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
LEFT, RIGHT = 0, 1
INDEX_NAME = {
    0: "Farmer", 1: "Fox", 2: "Chicken", 3: "Grain" # for __str__
}
COMBI_NAME = {'[0]': 'alone', '[0, 1]': 'with fox', '[0, 2]': 'with chicken', '[0, 3]': 'with grain'} # for formatting names of operators


class State:

    def __init__(self, d=None):
        if d==None:
            d = {
                'agents':[[],[]],
                'boat':LEFT
            }
        self.d = d

    def __eq__(self, s2):
        for prop in ['agents', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True
    
    def __str__(self):
        l = self.d['agents'][LEFT]
        r = self.d['agents'][RIGHT]
        txt = "\n Agents on the left side: "
        for a in l:
            txt += INDEX_NAME[a] + " "
        txt += "\n Agents on the right side: "
        for a in r:
            txt += INDEX_NAME[a] + " "
        side = 'left'
        if self.d['boat']==1: side = 'right'
        txt += "\n Boat is on the "+side+". \n"
        return txt


    def __hash__(self):
        return (self.__str__()).__hash__()
    
    def copy(self):
        news = State()
        news.d['agents'][LEFT] = [a for a in self.d['agents'][LEFT]] # deep copy of left side
        news.d['agents'][RIGHT] = [a for a in self.d['agents'][RIGHT]] # deep copy of right side
        news.d['boat'] = self.d['boat']
        return news
    
    def can_move(self, a):
        #useful for knowing where the farmer is
        side = self.d['boat']
        # possible moves will be:
            # farmer cross alone        [0]
            # farmer cross with fox     [0, 1]
            # farmer cross with chicken [0, 2]
            # farmer crosses with grain [0, 3]
        # check all agents are on the boat side
        for agent in a:
            if agent not in self.d['agents'][side]: return False
        # now check that the side will have any illegal states
        remaining =[x for x in self.d['agents'][side] if x not in a]
        remaining.sort() # sort to get in correct order to check illegal states
        if remaining == [1,2,3] or remaining == [1,2] or remaining == [2,3]: return False
        # if both pass this is a valid move
        return True
       
        
    def move(self, a):
        news = self.copy()  # create a deep copy
        side = self.d['boat'] # what side is the boat on
        new = [x for x in self.d['agents'][side] if x not in a] # create a new array of the ferry side with involved agents removed
        new.sort()
        news.d['agents'][side] = new # set that side to the new array
        for agent in a: # for agent involved in the move
            news.d['agents'][1-side].append(agent) # add the agent to the other side
            news.d['agents'][1-side].sort()
        news.d['boat'] = 1-side # move the boat
        return news
    
def goal_test(s):
    for _ in range(4):
        if _ not in s.d['agents'][RIGHT]: # if any 0-3 are not on right, return false
            return False
    return True

def goal_message(s):
    return "Congratulations! you successfully guided the fox, chicken, and grain across the river!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'agents':[[0, 1, 2, 3],[]], 'boat':LEFT })
#</INITIAL_STATE>

#<OPERATORS>
combinations = [[0], [0, 1], [0,2], [0,3]] # possible moving combinations


OPERATORS = [Operator(
    "Cross the river "+ COMBI_NAME.get(str(c)),
    lambda s, c1 = c: s.can_move(c1),
    lambda s, c1 = c: s.move(c1) )
    for c in combinations]
#</OPERATORS>


# Finish off with the GOAL_TEST and GOAL_MESSAGE_FUNCTION here.
GOAL_TEST = lambda s: goal_test(s)

GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)