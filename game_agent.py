"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

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
    # TODO: finish this function!
    # Return plus / minus infinity if the player wins or luses at the node.
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    # Return a combination of bellow computed scores:
    return custom_score_3(game, player)*0.25 + custom_score_2(game, player)*0.75

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
    # TODO: finish this function!
    # Return plus / minus infinity if the player wins or luses at the node.
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Get the blank and blocked spaces in the board. This is used to 
    # calculate weight of players own moves
    blank_space = float(len(game.get_blank_spaces()))
    blocked_space = float(game.width * game.height) - blank_space + 0.000001
    # Get players and it's opponents moces
    moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # Return a combination of players moves scaled by the game state (approximated by the blank space / blocked space)
    # minus the opponents moves. This combination should place more emphasis on minimizing opponents moves
    # the hurther we go to the game.
    return ((blank_space / blocked_space) * float(moves) * 2) - float(opp_moves)

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
    # TODO: finish this function!
    # Return plus / minus infinity if the player wins or luses at the node.
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    # Get location for the player and it's opponent
    location_player = game.get_player_location(player)
    location_oponent = game.get_player_location(game.get_opponent(player))
    
    def distance_players(p1, p2):
        """
        Function takes two players and return a squared distance between them.
        Parameters
        ----------
        p1 : Player one location on the board.

        p2 : Player two location on the board.

        Returns
        -------
        float
            squared distance between the players.
        """
        first = (p1[0] - p2[0])**2
        second = (p1[1] - p2[1])**2
        return float(first + second)
    # Apply the function and return the squared distance between the players.
    return distance_players(location_player, location_oponent)



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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

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

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # If this is the limit of depth, return score
        if depth == 0:
            return self.score(game, game.inactive_player)
        # Get all legal moves for the active player. 
        # if there is no legal moves -- return (-1, -1)
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        # Get the action associated with the max score.
        # This is a recursive all to the min and max functions defined bellow.
        _, action = max([(self.min(game.forecast_move(action), depth-1), action) for action in legal_moves])
        
        return action

    def min(self, game, depth):
        """
        Min function from AIMA text adjusted for search depth.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        """
        # Check if we still have time to perform search
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # If we are at the prespecified depth limit return score
        if depth == 0:
            return self.score(game, game.inactive_player)
        # Default value
        v = float('inf')
        # All legal moves
        legal_moves = game.get_legal_moves()
        # If there is no legal moves - return default value
        if not legal_moves:
            return v
        # For every legal action find the minimum value
        for action in legal_moves:
            v = min(v, self.max(game.forecast_move(action), depth-1))

        return v

    def max(self, game, depth):
        """
        Max function from AIMA text adjusted for search depth.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        """
        # Check if we still have time to perform search
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # If we are at the prespecified depth limit return score
        if depth == 0:
            return self.score(game, game.active_player)
        # Default value
        v = float('-inf')
        # All legal moves
        legal_moves = game.get_legal_moves()
        # If there is no legal moves - return default value
        if not legal_moves:
            return v
        # For every legal action find the maximum value
        for action in legal_moves:
            v = max(v, self.min(game.forecast_move(action), depth-1))

        return v


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

        # TODO: finish this function!
        # Implement iterative deepening -- start at depth = 0 and move deeper while 
        # We encounter SearchTimeout. At this point we return previously defined best move
        depth = 0
        while True:
            try:
                best_move = self.alphabeta(game, depth, alpha=float("-inf"), beta=float("inf"))
            except SearchTimeout:
                #  When we get SearchTimeout - break the cycle
                break 
            # Increase depth and calculate best_move again.
            depth += 1
        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

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

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

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

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # The best action if nothing works
        best_action = (-1, -1)
        # If we are at the limit of depth return score
        if depth == 0:
            return self.score(game, game.active_player)
        # Get all legal moves
        legal_moves = game.get_legal_moves()
        # If there is no legal moves reutrn defaul move (-1, -1)
        if not legal_moves:
            return best_action
        # Run through legal moves
        for action in legal_moves:
            # No need to have max here as in alphabeta_max function we are only interested in values!
            v = self.alphabeta_min(game.forecast_move(action), depth-1, alpha, beta)
            # Test if this is the best action so far
            if v > alpha:
                best_action = action
            # Adjust alpha value
            alpha = max(alpha, v)

        # Return action with the maximum value
        return best_action

    def alphabeta_max(self, game, depth, alpha, beta):
        """
        Max function from AIMA text adjusted for search depth.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        """
        # Check if we still have time to perform search
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # If we are at the limited depth -- return score
        if depth == 0:
            return self.score(game, game.active_player)
        # Default value
        v = float('-inf')
        # Get all legal moves
        legal_moves = game.get_legal_moves()
        # If there is no legal moves, return default value
        if not legal_moves:
            return v
        # For action in legal moves run the recursive calls and get the max value
        for action in legal_moves:
            v = max(v, self.alphabeta_min(game.forecast_move(action), depth-1, alpha, beta))
            # if we find value greater than beta - return it
            if v >= beta:
                return v
            # update alpha value
            alpha = max(alpha, v)

        return v

    def alphabeta_min(self, game, depth, alpha, beta):
        """
        Min function from AIMA text adjusted for search depth.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        """
        # Check if we still have time to perform search
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # If we are at the limited depth -- return score
        if depth == 0:
            return self.score(game, game.inactive_player)
        # Default value
        v = float('inf')
        # Get all legal moves
        legal_moves = game.get_legal_moves()
        # If there is no legal moves, return default value
        if not legal_moves:
            return v
        # For action in legal moves run the recursive calls and get the min value
        for action in legal_moves:
            v = min(v, self.alphabeta_max(game.forecast_move(action), depth-1, alpha, beta))
            # if we find value less than or equal to alpha - return it
            if v <= alpha:
                return v
            # Update beta
            beta = min(beta, v)

        return v
