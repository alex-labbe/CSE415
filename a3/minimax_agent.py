"""
minimax_agent.py
author: Alexandre Labbe
"""
import agent
import game
import copy
from threading import Thread
import time

X_PIECE = 'X'
O_PIECE = 'O'
EMPTY_PIECE = ' '
BLOCK_PIECE = '-'

class MinimaxAgent(agent.Agent):
    def __init__(self, initial_state: game.GameState, piece: str):
        super().__init__(initial_state, piece)
        self.valid_rows = set()
        self.time_up = False
        # take initial state board and create a dictionary of index to row of all possible rows
        # look at this dictionary and remove all the rows that are unable to produce a win



    def introduce(self):
        """
        returns a multi-line introduction string
        :return: intro string
        """
        return "My name is Toru Okada. \nI was created by Alexandre Labbe.\nI'm going to go sit in a well."

    def nickname(self):
        """
        returns a short nickname for the agent
        :return: nickname
        """
        return "Bird"

    def choose_move(self, state: game.GameState, time_limit: float) -> (int, int):
        """
        Selects a move to make on the given game board. Returns a move
        :param state: current game state
        :param time_limit: time (in seconds) before you'll be cutoff and forfeit the game
        :return: move (x,y)
        """
        if time_limit:
            start_time = time.time()
            depth = 1
            best_move = None
            self.time_up = False

            while not self.time_up:
                elapsed_time = time.time() - start_time
                if elapsed_time >= time_limit:
                    self.time_up = True
                    break

                move, _ = self.minimax(state, depth, time_limit - elapsed_time)
                if move is not None:
                    best_move = move
                depth += 1

            return best_move
        
        else:
            move, _ = self.minimax(state, 1)
            return move

        #return best_move[0]



    def minimax(self, state: game.GameState, depth_remaining: int, time_limit: float = None,
                alpha: float = None, beta: float = None, z_hashing=None) -> ((int, int), float):
        """
        Uses minimax to evaluate the given state and choose the best action from this state. Uses the next_player of the
        given state to decide between min and max. Recursively calls itself to reach depth_remaining layers. Optionally
        uses alpha, beta for pruning, and/or z_hashing for zobrist hashing.
        :param state: State to evaluate
        :param depth_remaining: number of layers left to evaluate
        :param time_limit: argument for your use to make sure you return before the time limit. None means no time limit
        :return: move (x,y) or None, state evaluation
        """

        if time_limit:
            start_time = time.time() # time limit

        #if at leaf based on ply, return the None for move, and the static eval of the state
        if depth_remaining == 0: return None, self.static_eval(state)

        provisional = 10**state.k
        if state.next_player == X_PIECE: provisional = -(10**state.k)

        move = None
        for s in self.generate_successors(state, state.next_player):
            if time_limit:
                elapsed_time = time.time() - start_time # time limit
            t_left = None
            if time_limit:
                if elapsed_time >= time_limit - 0.01:
                    self.time_up = True
                    break
                t_left = time_limit - elapsed_time
            newVal = self.minimax(s[0], depth_remaining-1, t_left)
            if self.time_up:
                break

            if((state.next_player == X_PIECE and newVal[1] > provisional) or (state.next_player == O_PIECE and newVal[1] < provisional)):
                provisional = newVal[1]
                move = s[1]

        return move, provisional
    

    def other_player(self, whose_move):
        if whose_move == X_PIECE:
            return O_PIECE
        return X_PIECE
    
    def generate_successors(self, state, whose_move):
        def new_board(board, i, j, whose_move):
            b = copy.deepcopy(board)
            b[i][j] = whose_move
            return b
        successors =  []
        k = state.k
        board = state.board
        n_rows = state.w
        n_col = state.h
        for i in range(n_rows):
            for j in range(n_col):
                if board[i][j] == EMPTY_PIECE:
                    new_state = game.GameState(new_board(board, i, j, whose_move), whose_move, k)
                    successors.append((new_state, (i, j)))
        return successors

    def static_eval(self, state: game.GameState) -> float:
        """
        Evaluates the given state. States good for X should be larger that states good for O.
        :param state: state to evaluate
        :return: evaluation of the state
        """
        if not self.valid_rows:
            self.populate_valid_rows(state)

        rows = self.get_rows(state.board)
        score = 0

        for row_index in self.valid_rows:
            row = rows[row_index]
            if X_PIECE in row and O_PIECE in row:
                continue
            c = row.count(X_PIECE) - row.count(O_PIECE)
            score += 10**(abs(c) - 1) * ((c > 0) - (c < 0))
        return score

    def populate_pboard(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != '-':
                    board[i][j]  = 'X'

    def populate_valid_rows(self, state):
        board = state.board
        possibilities_board = copy.deepcopy(board)
        self.populate_pboard(possibilities_board)
        possibilities = self.get_rows(possibilities_board)
        for i in range(len(possibilities)):
            r = possibilities[i]
            for str in r.split('-'):
                if len(str) >= state.k:
                    self.valid_rows.add(i)

    def get_rows(self, board):
        rows = [''.join(row) for row in board]
        cols = [''.join(col) for col in list(zip(*board))]
        h = len(board[0])
        w = len(board)

        diag_coords = [(i, i) for i in range(min(w, h))]
        left_diag_coords = [[(c[0], c[1] + i) for c in diag_coords if c[1] + i < h] for i in range(1, h)]
        right_diag_coords = [[(c[0] + i, c[1]) for c in diag_coords if c[0] + i < w] for i in range(1, w)]

        diags = [''.join(board[c[0]][c[1]] for c in diag_coords)]
        diags.extend([''.join(board[c[0]][h - 1 - c[1]] for c in diag_coords)])
        diags.extend([''.join(board[c[0]][c[1]] for c in coords) for coords in left_diag_coords])
        diags.extend([''.join(board[c[0]][h - 1 - c[1]] for c in coords) for coords in left_diag_coords])
        diags.extend([''.join(board[c[0]][c[1]] for c in coords) for coords in right_diag_coords])
        diags.extend([''.join(board[c[0]][h - 1 - c[1]] for c in coords) for coords in right_diag_coords])

        rows.extend(cols)
        rows.extend(diags)
        return rows

