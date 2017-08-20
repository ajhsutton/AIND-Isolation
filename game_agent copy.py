"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

# Line removed due to submission script
# from sample_players import improved_score, center_score

class SearchTimeout(Exception):
	"""Subclass base exception for code clarity. """
	pass

""" Default Heuristic Functions
Functions are included for fusion purposes in the custom_score_4 implementation.
Submission script will fail with import statement (commented in header).
"""

def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def center_score(game, player):
    """Outputs a score equal to square of the distance from the center of the
    board to the position of the player.

    This heuristic is only used by the autograder for testing.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)

""" Custom Heuristic Functions 
"""
# Pre-calculate the first and second order moves
directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
            	(1, -2), (1, 2), (2, -1), (2, 1)]   
second_order_directions = [(d1r + d2r, d1c + d2c) 
	for d1r, d1c in directions 
	for d2r, d2c in directions
	if d1r != -d2r and d1c != -d2c]    

def custom_score(game, player):
	"""Custom 1: Second Order moves via Direct Evaluation
	Calculate the heuristic value of a game state from the point of view
	of the given player. This heuristic sorce the game state based upon the number 
	of 2nd order moves available to a player. 
	
	This function forcasts the game state after execution of each move.

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
		The number of moves available to a player after then next move.
	"""
	# Win/Loss Check
	if game.is_loser(player):
		return float("-inf")

	if game.is_winner(player):
		return float("inf")
	
	# Generate score for Player and Opponent
	player_score = getSecondOrderMoveCount(game, player)
	opponent_score = getSecondOrderMoveCount(game, game.get_opponent(player))
	return player_score - opponent_score

def getSecondOrderMoveCount(game, player):
	""" Helper function
	Evaluate the number of second order moves available
	to a player. The specific moves are pre-calulated.
	"""
	r,c = game.get_player_location(player)	
	valid_move_count = sum([game.move_is_legal((r + dr, c + dc)) 
						for dr, dc in second_order_directions])
	if valid_move_count:
		return float(valid_move_count)
	else:
		# No moves are available
		return float("-inf")
		
def custom_score_2(game, player):
	""" Second Order moves via ‘Full’ Evaluation
	Calculate the heuristic value of a game state from the point of view
	of the given player. This heuristic sorce the game state based upon the number 
	of 2nd order moves available to a player. 
	
	This function forcasts the game state after execution of each move by evaluating
	a sub-tree of game states.

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
		The number of moves available to a player after then next move.
	"""
	
	# Win/Loss Check
	if game.is_loser(player):
		return float("-inf")

	if game.is_winner(player):
		return float("inf")
	
	score = 0
	
	player_pos = game.get_player_location(player)
	opponent_pos = game.get_player_location(game.get_opponent(player))
	
	own_moves = game.get_legal_moves(player)
	opp_moves = game.get_legal_moves(game.get_opponent(player))
	
	# Player Score
	for mv in own_moves:
		play_pred_game = game.forecast_move(mv)
		score += improved_score(play_pred_game, player)
		if score == float("inf") or score == float("-inf"):
			return score
			
	# Opponent Score
	game_opp = game.forecast_move(player_pos)
	for mv in opp_moves:
		opp_pred_game = game_opp.forecast_move(mv)
		score -= improved_score(opp_pred_game, opp_pred_game.get_opponent(player))
		if score == float("inf") or score == float("-inf"):
			return score
	
	return float(score)

def is_reflectable_pos(pos):
	return pos in [(2,1),(2,1),(4,5),(5,4),(4,1),(1,4),(5,2),(2,5)]

def custom_score_3(game, player):
	"""Calculate the heuristic value of a game state from the point of view
	of the given player. This heuristic expands custom_score by inclusion of 
	'early game' mechanics for move selection and centering of position.

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
	if game.move_count < 2:
		# if center is available, take the center
		pos = game.get_player_location(player)
		if pos[0] == 3 and pos[1] == 3:
			return float("inf")
		elif opp_pos[0] == 3 and opp_pos[1] == 3:
			# If the Opponent has the center, take any position that cannot be 'reflected'
			# from the center position
			if is_reflectable_pos(pos):
				return float("-inf")
	elif game.move_count < 10:
		return custom_score(game, player) + (10 - game.move_count) * center_score(game, player)
	else:
		return custom_score(game, player)
		
def custom_score_4(game, player):
	"""Calculate the heuristic value of a game state from the point of view
	of the given player. This heuristic implements a fusion of three 
	heuristic functions:
		- improved_score: calculation of the relative number of 'first 
			order' moves.
		- custom_score: calculation of the relative number of 'second 
			order' moves.
		- center_score: value favoring centering.

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
	return float(improved_score(game, player)
			 + 0.5 * custom_score(game, player)
			 + 0.5 * center_score(game, player))

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

	def minimax(self, game, depth = 1):
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
		
		# Implement Timer for Competition Agents
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
			
		# Minimax Algorithm
		# Maximize utility for the current state
		legal_moves = game.get_legal_moves(self)
		
		if len(legal_moves) == 0:
			return (-1,-1)
			
		best_move = legal_moves[0]
		best_score = -float("inf")

		# Evaluate the best legal move, based upon the min score 
		for lm in legal_moves:
			forcast_game = game.forecast_move(lm)
			move_score = self.min_score(forcast_game, depth - 1)
			if move_score > best_score:
				best_score = move_score
				best_move = lm		
		
		# Return the minimax decision: the action that maximizes the metric.
		return best_move
		
	def max_score(self, game, depth):
		# Evaluate the min-level for the game board for the inactive player move.
		
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
		
		if depth == 0:
			# Evaluate the result on the current state.
			return self.score(game, self)
		else:
			# Generate Legal Moves for the Player
			legal_moves = game.get_legal_moves(self)
			
			# if ~legal_moves:
			# 	return game.utility(self)
			
			# Default Return
			best_score = float("-inf")
			
			# Maximize the results of a min-node
			for lm in legal_moves:
				# Expand the minimax tree to the next level
				forcast_game = game.forecast_move(lm)
				move_score = self.min_score(forcast_game, depth - 1)
				if move_score > best_score:
					best_score = move_score
			return best_score
		
	def min_score(self, game, depth):
		# Evaluate the min-level for the game board for the inactive player move.
		
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
		
		if depth == 0:
			# Evaluate the result on the current state.
			return self.score(game, self)
		else:			
			# Generate Legal Moves for the Opposition
			legal_moves = game.get_legal_moves(game.get_opponent(self))
			
			# Default Return
			best_score = float("inf")

			# Minimize the results of a max-node
			for lm in legal_moves:
				# Expand the minimax tree to the next level
				forcast_game = game.forecast_move(lm)
				move_score = self.max_score(forcast_game, depth - 1)
				if move_score < best_score:
					best_score = move_score
			return best_score	

class AlphaBetaPlayer(IsolationPlayer):
	"""Game-playing agent that chooses a move using iterative deepening minimax
	search with alpha-beta pruning. You must finish and test this player to
	make sure it returns a good move before the search time limit expires.
	"""
	itrdeep = 1

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
		
		# Initialize the best move so that this function returns something
		# in case the search fails due to timeout
		best_move = (-1, -1)
		
		# Iterative Deepening
		# Record the best move for each search depth
		
		search_depth = 1;
		while(self.itrdeep):
			try:
				# The try/except block will automatically catch the exception
				# raised when the timer is about to expire.
				best_move =  self.alphabeta(game, search_depth)
				search_depth = search_depth + 1
			except SearchTimeout:
				return best_move
		
		# Bypass Iterative Deepening
		try:
			# The try/except block will automatically catch the exception
			# raised when the timer is about to expire.
			print('AB-Bypass')
			best_move =  self.alphabeta(game, self.search_depth)
		except SearchTimeout:
			return best_move
		
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
			
		# Implement Timer for Competition Agents
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
								
		# Generate Legal Moves for the Player
		legal_moves = game.get_legal_moves(self)
		if len(legal_moves) == 0:
			return (-1,-1)
		
		best_move = legal_moves[0]
		best_score = float("-inf")
		
		# Maximize the results of a min-node
		for lm in legal_moves:
			# Expand the minimax tree to the next level
			forcast_game = game.forecast_move(lm)
			v = self.ab_min_score(forcast_game, depth - 1, alpha, beta);
			if v > best_score:
				best_move = lm
				best_score = v
			alpha = max([alpha, best_score])
			
			if best_score == float("inf"):
				# Optimal Move Identified: terminate search
				# Introduction of termination permits 'early game' triggers 
				# in the heuristic function, such as center-selection.
					return best_move
		return best_move
	
	def ab_max_score(self, game, depth, alpha=float("-inf"), beta=float("inf")):
		# Evaluate the max-value for the game using assumes alpha-beta pruning.		
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
		
		if depth <=0 :
			# Evaluate the result on the current state.
			return self.score(game, self)
		else:
			# Default Return
			v = float("-inf")
			
			# Generate Legal Moves for the Player
			legal_moves = game.get_legal_moves()
			
			# Maximize the results of a min-node
			for lm in legal_moves:
				# Expand the minimax tree to the next level
				forcast_game = game.forecast_move(lm)
				v = max([v, self.ab_min_score(forcast_game, depth - 1, alpha, beta)]);
				if v >= beta:
					return v
				alpha = max([alpha, v])
			return v
		
	def ab_min_score(self, game, depth, alpha=float("-inf"), beta=float("inf")):
		# Evaluate the min-value for the game using assumes alpha-beta pruning.
		if self.time_left() < self.TIMER_THRESHOLD:
			raise SearchTimeout()
		
		if depth <=0 :
			# Evaluate the result on the current state.
			return self.score(game, self)
		else:
			# Default Return
			v = float("inf")
			
			# Generate Legal Moves for the Player
			legal_moves = game.get_legal_moves()
			
			# Maximize the results of a min-node
			for lm in legal_moves:
				# Expand the minimax tree to the next level
				forcast_game = game.forecast_move(lm)
				v = min([v, self.ab_max_score(forcast_game, depth - 1, alpha, beta)]);
				if v <= alpha:
					return v
				beta = min([beta, v])	
			return v