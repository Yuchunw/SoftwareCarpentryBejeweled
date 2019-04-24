# This code is for defining function in our game.

## INCOMPLETED!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

import pygame, random, time, sys, itertools, os
from setup import *


class cell:
	# Cell on the board 
	# Properties: 'image' and etc..
	# Add properties of cell here!
	def _init_(self, image):
		self.offset = 0.0
		self.image = monsters

	 def tick(self, dt):
	 	self.offset = max(0.0, self.offset - dt * refillspeed)

class board:
	# A rectangular board of cells
	# Properties: width, height, size and etc...
	def _init_(self, width, height):
		self.width = boardwidth
		self.height = boardheight
		self.size = boardheight * boardwidth
		self.board = [cell(self.blank) for _ in range(self.size)]
		self.matches = []
		self.refill = []

	def generate(self):
		for i in range(self.size):
			self.board[i] = cell(random.choice(self.image))

	def freeze(self):
		# If the board is busy animating a refill or sth, refuse swaps
		return self.refill or self.matches

	def pos(self, i, j):
		# Index of cell positions
		if (0 <= i < self.width) and (0 <= j < self.height):
			return j * self.width + i
		return None

	def findmatch(self):
		# Check matches
		def lines():
			for j in range (self.height):
				yield range(j * self.width, (j + 1) * self.width)
			for i in range (self.width):
				yield range(i, self.size, self.width)
		def key(i):
			return self.board[i].image
		def matches():
			for line in lines():
				for _, group in itertools.groupby(line, key):
					match = list(group)
					if len(match) >= matchmin:
						yield match
		return list(matches())

	def updatematch(self, image):
		# Replace cells in match with other images
		for match in self.matches:
			for position in match:
				self.board[position].image = image

	def refill(self):
		# Cells drop to fill the blank and creat neww cells if necessary
		for i in range(self.width):
			target = self.size - i -1
			for pos in range(target, -1, -self.width):
				if self.board[pos].image != self.blank:
					c = self.board[target]
					c.image = self.board[pos].image
					c.offset = (target - pos) // self.width
					target -= self.width
					yield c
			offset = 1 + (target - pos) // self.width
			for pos in range(target, -1, -self.width):
				c = self.board[pos]
				c.image = random.choice(self.image)
				c.offset = offset
				yield c




class Game:
	# State of the game
	# Propteries: clock, display, font, board, score and etc..
	def _init_(self):
		self.board_size = 9
		self.gems = [0, 1, 2, 3]
		self.game_board = None
		self.start_coords = set()

	# def start(self):
	# 	# Start a new game
	# 	self.board.generate()
	# 	self.score = 0.0
	# 	self.swap_time = 20.0

	# def quit(self):
	# 	# Quit the game
	# 	pygame.quit()
	# 	sys.exit()

	# def play(self):
	# 	self.start()
	# 	while True:
	# 		self.draw()
	# 		dt = min(self.clock.tick(fps) / 1000.0, 1.0 / fps)
	# 		self.swap_time += dt
	# 		for event in pygame.event.get()
	# 			if event.type == pygame.QUIT:
	# 				self.quit()

	def play(self):
		

	def basic_score(self, cell_type):
		if cell_type in self.gems:
			return 1
		return 0

	def score(self, board, cells_coords):
		score = 0
		for coords in cells_coords:
			cell_type = board[coords[0]][coords[1]]
			score += self.basic_score(cell_type)

		if len(cells_coords) == 4:
			score += 5
		if len(cells_coords) == 5:
			score += 10
		return score

	def drawtime(self):
		t = int(self.swap_time)
		text = self.font.render('Mover Timer: {}:{:02}'.format(t / 60, t % 60), True, black)
		self.display.blit(text, (offset, boardheight - fontsize))

	def drawscore(self):
		t = self.score + self.board.scire
		text = self.font.render('Score: {}'.format(t), True, black)
		self.display.blit(test, (offset, boardheight - fontsize))


# To do list!!!
# Define Time
# Define Gem match
# Define Gem Disappear
# Define Gem drop down
