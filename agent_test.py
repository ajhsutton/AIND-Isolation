"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
	"""Unit tests for isolation agents"""
	
	def setUp(self):
		reload(game_agent)
		self.player1 = game_agent.MinimaxPlayer(search_depth = 2)
		self.player2 = game_agent.MinimaxPlayer(search_depth = 2)
		self.game = isolation.Board(self.player1, self.player2)

	def minimax_player_setup(self):
		# place player 1 on the board at row 2, column 3, then place player 2 on
		# the board at row 0, column 5; display the resulting board state.  Note
		# that the .apply_move() method changes the calling object in-place.
		# Test player positions and active status after call
		self.setUp()
		
		self.game.apply_move((2, 3))
		# Test P2 is active
		self.assertTrue(self.game.active_player == self.player2)
		self.game.apply_move((0, 5))
		# Test P1 is active
		self.assertTrue(self.game.active_player == self.player1)

		
	def test_player_setup(self):
		# Test Player Positions
		self.minimax_player_setup()
		
		(h1,w1) = self.game.get_player_location(player = self.player1)
		self.assertTrue((h1,w1) == (2,3),"Player 1 Position Error")
		(h2,w2) = self.game.get_player_location(player = self.player2)
		self.assertTrue((h2,w2) == (0,5),"Player 2 Position Error")
		
	def test_get_moves(self):
		# Test Available Moves for player 1
		self.minimax_player_setup()
		
		LM1 = self.game.get_legal_moves()
		self.assertTrue(len(LM1) == 8,"Player 1 Moves remaining error: 8 expected")
		LM2 = self.game.get_legal_moves(self.game.inactive_player)
		self.assertTrue(len(LM2) == 3,"Player 2 Moves remaining error: 3 expected")
		
	def test_move_forcast(self):
		# Test the return for forcasting moves
		self.minimax_player_setup()
		
		legal_moves = self.game.get_legal_moves()
		self.game.apply_move(legal_moves[1])
		p1_pos = self.game.get_player_location(self.player1)
		self.assertTrue(p1_pos == legal_moves[1],
			"Player 1 Move error")
			
	def test_minimax1(self):
		print('Running Minimax Test')
		self.minimax_player_setup()	
		print(self.game.to_string())
		
		time_left = lambda:1000
		
		# Evaluate Minimax function
		mv = self.player1.get_move(self.game, time_left)
# 		assert(self.game.move_is_legal(mv),'Illegal Move Selected')
		self.game.apply_move(mv);
		print(self.game.to_string())

		mv = self.player2.get_move(self.game, time_left)
# 		assert(self.game.move_is_legal(mv),'Illegal Move Selected')
		self.game.apply_move(mv);
		print(self.game.to_string())


	def test_play_game_minimax(self):
		self.minimax_player_setup()
		winner, history, outcome = self.game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(self.game.to_string())
		print("Move history:\n{!s}".format(history))
		

if __name__ == '__main__':
	unittest.main()