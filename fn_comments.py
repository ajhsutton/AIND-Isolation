
	
	
	
	"""Custom 2: Second Order moves via ‘Full’ Evaluation
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
	
	
	
	
	"""Calculate the heuristic value of a game state from the point of view
	of the given player. This heuristic expands custom_score by inclusion of 
	'early game' mechanics for move selection and centering of position.
	
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
	
	
	"""Calculate the heuristic value of a game state from the point of view
	of the given player. This heuristic implements a fusion of three 
	heuristic functions:
		- improved_score: calculation of the relative number of 'first 
			order' moves.
		- custom_score: calculation of the relative number of 'second 
			order' moves.
		- center_score: value favoring centering.

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