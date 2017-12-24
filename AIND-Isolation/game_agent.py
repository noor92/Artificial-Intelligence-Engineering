import random
import math

# code used in the custom_score functions #

def all_player_moves(game, player):
    '''returns all the moves availble fo each player'''
    return game.get_legal_moves(player),game.get_legal_moves(game.get_opponent(player))

def players_locations(game, player):
    '''returns the location available for each player'''
    return game.get_player_location(player), game.get_player_location(game.get_opponent(player))

def corder_edge_moves(game, moves):
    '''returns the edge and corner moves available'''
    counter=0
    for row, column in moves:
        if row == 0:
            counter +=1
        if column == 0:
            counter +=1
        if row == game.height:
            counter+=1
        if column == game.width:
            counter+=1
    return counter




class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    '''
    This heuristic limits future opponent moves by assigning a higher evaluation
    function to a game state if the possibility of future moves is scarce, and a lower 
    evaluation function if the possibiliyt of future moves is plenty. In the classes, this
    was mentioned as #myMoves-2* #opponentMoves.

    Here, the weight of 2 with the opposition legal moves means we are penalizing
    highly for a board state, where the opponent has more moves at it's disposal.
    We will be inclined to choosing the board states in which the opponent is
    fairly limited in in it's movements.'''
    
    player_legal_moves=game.get_legal_moves(player)
    total_moves=len(player_legal_moves)

    for move in player_legal_moves:
        board=game.forecast_move(move)
        total_moves+=len(board.get_legal_moves())

    opp_player_legal_moves=game.get_legal_moves(game.get_opponent(player))
    opp_total_moves=len(opp_player_legal_moves)

    for opp_move in opp_player_legal_moves:
        board=game.forecast_move(opp_move)
        opp_total_moves+=len(board.get_legal_moves())

    return(float(total_moves - 2*opp_total_moves))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    """ 
    This heuristic finds the difference in player moves and an opponent's moves 
    based on the distance between both players. The evaluation will help 
    decide which moves are least favorable (penalty moves).
    """

    player_moves, opp_player_moves= all_player_moves(game, player)
    player_location, opp_player_location=players_locations(game,player)
    distance_between_players=float(abs(player_location[0]-opp_player_location[0]) +  abs(player_location[1]-opp_player_location[1]))

    player_penalty_move=corder_edge_moves(game, player_moves)
    opponent_penalty_move=corder_edge_moves(game, opp_player_moves)

    player=len(player_moves) - 0.5* player_penalty_move
    opp_player=len(opp_player_moves) - 0.5* opponent_penalty_move

    return (player - opp_player) * distance_between_players



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
   
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
       

    '''
    This heuristic focuses on aagressively chasing the opponent. 
    '''

    player_moves = len(game.get_legal_moves(player))
    opp_player_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(abs(player_moves - 2*opp_player_moves))
 

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        if self.search_depth==0:
            return (None,self.score(game,self))

        legal_moves=game.get_legal_moves()

        if len(legal_moves) == 0:
            return (-1, -1)

        if len(legal_moves) == 1:
            return legal_moves[0]

        self.best_move = legal_moves[0]

        try:
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            return self.best_move 
        return self.best_move


    def minimax(self, game, depth):

        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper fuctions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def min_max(game,depth):

            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if depth==0:
                return (None,self.score(game,self))

            legal_moves = game.get_legal_moves()

            if legal_moves == []:
                return ((-1,-1))

            best_move=legal_moves[0]

            if game.active_player== self:
                v = float("-inf")
                player_move=max
            else:
                v = float("inf")
                player_move=min

            for move in legal_moves:
                forecast_m = min_max(game.forecast_move(move),depth-1)[1]
                if player_move(v, forecast_m) == forecast_m:
                    best_move=move
                    v=player_move(v,forecast_m)

            return (best_move,v)
        return min_max(game,depth)[0]




   


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        legal_moves=game.get_legal_moves()

        if len(legal_moves) == 0:
            return (-1, -1)

        if len(legal_moves) == 1:
            return legal_moves[0]

        self.best_move = legal_moves[0]

        depth=1

        while True:
            try:
                for depth in range(100):
                    self.best_move = self.alphabeta(game, depth, alpha=float('-inf'), beta=float('inf'))

            except SearchTimeout:
                return self.best_move
                

            return self.best_move


    def maximum_value(self, game, depth ,alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        if depth == 0:
             return self.score(game, self)
            
        v = float("-inf")

        for move in game.get_legal_moves(game.active_player):
            v = max(v, self.minimum_value(game.forecast_move(move),depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)   
        return v

    
    def minimum_value(self, game,depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        
        if depth == 0:
            return self.score(game, self)


        v = float("inf")

        for move in game.get_legal_moves(game.active_player):
            v = min(v, self.maximum_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
      
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if not  game.get_legal_moves():
            return ((-1,-1))

        if depth == 0:
            return self.score(game, game.active_player)


        best_score= float("-inf")
        best_move =  ((-1,-1))

        for move in game.get_legal_moves():
            v = self.minimum_value (game.forecast_move(move), depth-1, alpha, beta)
            if v > best_score:
                best_score = v
                best_move = move
            alpha = max(alpha, v)   
        return best_move



       
