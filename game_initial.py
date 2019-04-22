# This code is for defining function in our game.

## INCOMPLETED!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

gems = {0: 'red', 1: 'green', 2: 'blue' , 3:'yellow'}

class GemGame:
	def _init_(self):
		self.board_size = 9
		self.gems = [0, 1, 2, 3]
		self.game_board = None
		self.start_coords = set()

	def basic_score(self, gem_type):
		if gem_type in self.gems:
			return 1
		return 0

	def score(self, board, gems_coords):
		score = 0
		for coords in gems_coords:
			gem_type = board[coords[0]][coords[1]]
			score += self.basic_score(gem_type)

		if len(gems_coords) == 4:
			score += 5
		if len(gems_coords) == 5:
			score += 10
		return score

# Define Time
# Define Gem match
# Define Gem Disappear
# Define Gem drop down
