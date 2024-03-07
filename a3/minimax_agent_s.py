"""
minimax_agent.py
author: Chukwuemeka Mordi
"""
import agent
import game


class MinimaxAgent(agent.Agent):
    def __init__(self, initial_state: game.GameState, piece: str):
        super().__init__(initial_state, piece)
        
        """ 
        would make initializations here but doesnt really make that much sense in my current program since minimax 
        needs refresed values for each call and im not sharing variables between methods
        """

    def introduce(self):
        """
        returns a multi-line introduction string
        :return: intro string
        """
        #NOTE: had to return multi line string since I failed the test
        return ("Hey, Chukwuemeka Mordi (uwnetid: cmordi),\n"+
        "It is PaulDurham here, I am your agent for this game.\n"+
        "I hope you and I can tackle this challenge together!")

    def nickname(self):
        """
        returns a short nickname for the agent
        :return: nickname
        """
        return "PaulDurham"

    def choose_move(self, state: game.GameState, time_limit: float) -> (int, int):
        """
        Selects a move to make on the given game board. Returns a move
        :param state: current game state
        :param time_limit: time (in seconds) before you'll be cutoff and forfeit the game
        :return: move (x,y)
        """
        #NOTE: remove or update time limit if program fails
        #NOTE: "time_limit" is in seconds
        optimal_move, _ = self.minimax(state, depth_remaining = 3)    
        return optimal_move

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
        #NOTE: dont know if I should be using time limit here
        
        # base case
        if state.winner() is not None or depth_remaining == 0:
            return None, self.static_eval(state)

        if state.next_player == game.X_PIECE:
            optimal_move = None
            maxi = float('-inf')
            for m in self.possible_moves(state):
                next_state = state.make_move(m)
                _, curr_eval = self.minimax(next_state, depth_remaining-1)    #recursive calls here, so might be slow. if it is look into the time limit
                if curr_eval > maxi:
                    optimal_move = m
                    maxi = curr_eval
            return optimal_move, maxi
        
        else:
            optimal_move = None
            mini = float('inf')
            for m in self.possible_moves(state):
                next_state = state.make_move(m)
                _, curr_eval = self.minimax(next_state, depth_remaining-1)    #recursive calls here, so might be slow. look into the time limit
                if curr_eval < mini:
                    optimal_move = m
                    mini = curr_eval
            return optimal_move, mini
        
        #return (0, 0), 0.0

    def static_eval(self, state: game.GameState) -> float:
        """
        Evaluates the given state. States good for X should be larger that states good for O.
        :param state: state to evaluate
        :return: evaluation of the state
        """
        track_x, track_o = 0, 0
        
        for r in state.board:
            for c in r:
                if c == game.X_PIECE:
                    track_x += 1
                elif c == game.O_PIECE:
                    track_o += 1
        return track_x - track_o
    
    # Helper to simulate possible moves
    def possible_moves(self, state: game.GameState):
        available_moves = []
        for i in range(state.w):
            for j in range(state.h):
                if state.board[i][j] == game.EMPTY_PIECE: available_moves.append((i, j))
        return available_moves
