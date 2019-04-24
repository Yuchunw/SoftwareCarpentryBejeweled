# This code is for defining function in our game.

## INCOMPLETED!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

import pygame, random

gems = {0: 'red', 1: 'green', 2: 'blue' , 3:'yellow'}

class cell:
	# Cell on the board 
	# Properties: 'image' and etc..
	# Add properties of cell here!
	def _init_(self, image):
		self.offset = 0.0
		self.image = image


class board:
	# A rectangular board of cells
	# Properties: width, height, size and etc...
	def _init_(self):



class Game:
	# State of the game
	# Propteries: clock, display, font, board, score and etc..
	def _init_(self):
		self.board_size = 9
		self.gems = [0, 1, 2, 3]
		self.game_board = None
		self.start_coords = set()

	def precheck(self):
		rotated_board = list(map(list, zip(* self.board))):
		for y in range(len(self.board)):
			sy = ''.join([numbers_to_letters[x] for x in self.board[y]])
			sx = ''.join([numbers_to_letters[x] for x in rotated_board[y]])
			for formula in formulas.keys():
				if formula in sx:
					self.board[sx.find(formula)][y] = random.randint(0, 1)

				elif formula in sy:
					self.board[y][sy.find(formula)] = random.randint(0, 1)

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


# To do list!!!
# Define Time
# Define Gem match
# Define Gem Disappear
# Define Gem drop down
