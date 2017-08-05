"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class ABIsolationTest(unittest.TestCase):
	"""Unit tests for isolation agents"""
	
	def setUp(self):
		reload(game_agent)
		self.player1 = game_agent.AlphaBetaPlayer(search_depth = 2)
		self.player2 = game_agent.AlphaBetaPlayer(search_depth = 2)
		self.game = isolation.Board(self.player1, self.player2)

	def ab_player_setup(self):
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
			
	def test_alphabeta(self):
		print('Running Alpha-Beta Test')
		self.ab_player_setup()	
		print(self.game.to_string())
		
		
		time_left = lambda: 1000
		# Evaluate Minimax function
		num_turns = 4
		for t in range(num_turns):
			print('Turn :' + str(t+1))
			mv = self.player1.get_move(self.game, time_left)
			assert(self.game.move_is_legal(mv),'P1 Illegal Move Selected')
			self.game.apply_move(mv);
			print(self.game.to_string())

			mv = self.player2.get_move(self.game, time_left)
			assert(self.game.move_is_legal(mv),'P2 Illegal Move Selected')
			self.game.apply_move(mv);
			print(self.game.to_string())

	def test_play_game_alphabeta(self):
		self.ab_player_setup()
		winner, history, outcome = self.game.play()
		print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
		print(self.game.to_string())
		print("Move history:\n{!s}".format(history))

if __name__ == '__main__':
	unittest.main()