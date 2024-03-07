"""
minimax_agent.py
author: Jared Yoder & Lucy Camblin
"""
import agent
import game
import re
import math
import time

"""
Use these globals below for good programming practices instead of hard coding 'X' or 'O' into your code.
"""
X_PIECE = 'X'
O_PIECE = 'O'
BLOCK_PIECE = '-'
EMPTY_PIECE = ' '

class MinimaxAgent(agent.Agent):
    def __init__(self, initial_state: game.GameState, piece: str):
        super().__init__(initial_state, piece)

    def introduce(self):
        """
        returns a multi-line introduction string
        :return: intro string
        """
        return ("Agent: Ol' Feller\n" +
                "by Jared Yoder (jmyoder) & Lucy Camblin (lcambl)\n" +
                "BARK LIKE A DOG, YER BELOW ME\n")

    def nickname(self):
        """
        returns a short nickname for the agent
        :return: nickname
        """
        return "Ol' Feller"

    def choose_move(self, state: game.GameState, time_limit: float) -> (int, int):
        """
        Selects a move to make on the given game board. Returns a move
        :param state: current game state
        :param time_limit: time (in seconds) before you'll be cutoff and forfeit the game
        :return: move (x,y)
        """
        depth = 1
        move, value = self.minimax(state, depth, time_limit, -math.inf, math.inf)
        print("choosing the move " + str(move))
        if move is None:
            move = successors(state)[0]
        return move

    def minimax(self, state: game.GameState, depth_remaining: int, time_limit: float = None,
                alpha: float = None, beta: float = None, z_hashing=None) -> ((int, int), float):
        """
        Uses minimax to evaluate the given state and choose the best action from this state. Uses the next_player of the
        given state to decide between min and max. Recursively calls itself to reach depth_remaining layers. Optionally
        uses alpha, beta for pruning, and/or z_hashing for zobrist hashing.
        :param state: State to evaluate
        :param depth_remaining: number of layers left to evaluate
        :param time_limit: argument for your use to make sure you return before the time limit. None means no time limit
        :param alpha: alpha value for pruning
        :param beta: beta value for pruning
        :param z_hashing: zobrist hashing data
        :return: move (x,y) or None, state evaluation
        """
        start = time.time()

        result = None
        move = None
        if depth_remaining == 0:
            result = self.static_eval(state)
            print("static eval is " + str(result))
            return move, result
        else:
            if state.next_player is X_PIECE:
                result = -100000
            else:
                result = 100000
        for s in successors(state):
            end = time.time()
            change = end - start
            if time_limit is not None:
                if time_limit - change < 0.03:
                    print("Outta time foo")
                    break
                else:
                    time_limit -= change
            dummy, newVal = self.minimax(state.make_move(s), depth_remaining - 1, time_limit, alpha, beta)
            #print ("move is " + str(s) + "\n")

            if alpha is not None and beta is not None:
                #TODO this is an attempt at alpha beta
                if self.piece == X_PIECE:
                    # this means we are maximizing player, update beta when depth remaining is odd
                    if depth_remaining % 2:
                        if newVal < beta: beta = newVal
                    else:
                        if newVal > alpha: alpha = newVal
                else:
                    # this means we are minimizing player, update beta when depth remaining is even
                    if (depth_remaining % 2) == 0:
                        if newVal < beta: beta = newVal
                    else:
                        if newVal > alpha: alpha = newVal
                # determine if we should perform a cutoff
                if cutoff(alpha, beta):
                    return move, result


            if (state.next_player == X_PIECE) and (newVal > result)\
                    or (state.next_player == O_PIECE) and (newVal < result):
                result = newVal
                move = s
                #print("new move is " + str(s) + "\n")
        print("returning move " + str(move) + " and result " + str(result) + "\n")
        if move is None:
            print("Why is move None!\n")
        return move, result

    def static_eval(self, state: game.GameState) -> float:
        """
        Evaluates the given state. States good for X should be larger that states good for O.
        :param state: state to evaluate
        :return: evaluation of the state
        """
        rows = gen_search_grid(state)
        v = 0

        for r in rows:
            if re.search(f'[{X_PIECE}]{{{state.k}}}', r):
                return math.inf
            if re.search(f'[{O_PIECE}]{{{state.k}}}', r):
                return -math.inf

            #print(str(state.board))
            # find all non-blocked X sections of a row
            unblocked = re.findall(rf'[X ]{{{state.k},}}', r)
            for section in unblocked:
                countx = num_pieces(X_PIECE, section)
                #print(re.search(f'[{EMPTY_PIECE}]{{{state.k-1}}}', r))
                v += 10**countx

            # find all non-blocked O sections of a row
            unblocked = re.findall(f'[{EMPTY_PIECE}{O_PIECE}]{{{state.k},}}', r)
            for section in unblocked:
                counto = num_pieces(O_PIECE, section)
                # print(re.search(f'[{EMPTY_PIECE}]{{{state.k-1}}}', r))
                v -= 10**counto

        return v


def num_pieces(piece, match):
    #max = 0
    count = 0
    for letter in match:
        if letter == piece:
            count += 1
    return count


def successors(state: game.GameState):
    moves = []
    for x in range(len(state.board)):
        for y in range(len(state.board[x])):
            if is_empty(state, (x, y)):
                moves.append((x, y))
    return moves


def gen_search_grid(state: game.GameState):
    rows = [''.join(row) for row in state.board]
    cols = [''.join(col) for col in list(zip(*state.board))]

    diag_coords = [(i, i) for i in range(min(state.w, state.h))]
    left_diag_coords = [[(c[0], c[1] + i) for c in diag_coords if c[1] + i < state.h] for i in range(1, state.h)]
    right_diag_coords = [[(c[0] + i, c[1]) for c in diag_coords if c[0] + i < state.w] for i in range(1, state.w)]

    diags = [''.join(state.board[c[0]][c[1]] for c in diag_coords)]
    diags.extend([''.join(state.board[c[0]][state.h - 1 - c[1]] for c in diag_coords)])
    diags.extend([''.join(state.board[c[0]][c[1]] for c in coords) for coords in left_diag_coords])
    diags.extend([''.join(state.board[c[0]][state.h - 1 - c[1]] for c in coords) for coords in left_diag_coords])
    diags.extend([''.join(state.board[c[0]][c[1]] for c in coords) for coords in right_diag_coords])
    diags.extend([''.join(state.board[c[0]][state.h - 1 - c[1]] for c in coords) for coords in right_diag_coords])

    rows.extend(cols)
    rows.extend(diags)

    return rows

def is_empty(state: game.GameState, move: (int, int)):
    return state.board[move[0]][move[1]] is EMPTY_PIECE

def cutoff(alpha, beta):
    if alpha >= beta: return True
    return False

