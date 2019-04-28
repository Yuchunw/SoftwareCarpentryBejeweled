# This code is for defining function in our game.

## INCOMPLETED!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

import pygame, random, time, sys, itertools, os, copy


# Set up the screen
size = (400, 534)


# To manage how fast the screen updates
clock = pygame.time.Clock()
timer = 20
dt = 0



# Load the background image
background = pygame.image.load('Gameboard.png').convert()
# Load the monsters image
monsters = [pygame.image.load('Monster{}.png'.format(i)) for i in range (1, 6)]
# Load tha blank image
blank = pygame.image.load('Blank.png').convert()

# Parameters for Draw board on screen
boardwidth = 364
boardheight = 363
columns = 8
rows = 8
black = (0, 0, 0)
start_x = 20
start_y = 160
end_x = start_x + boardwidth - 1
end_y = start_y + boardheight - 1
columns = 8
rows = 8
monster_size = 64
empty_space = -1

# Other parameters
fps = 60
fontsize = 30
font = pygame.font.SysFont('Consolas', 30)
# offset = 5
refillspeed = 10



# Rules for Game
matchmin = 3

# Game sounds
# 1 for background; 2 for swipe; 3 for combo; 4 for wrong; 5 for clock 
# sounds = []
# for i in range(1, 6):
# 	sounds.append(pygame.mixer.music.load('Sound%s.wav' % i))


class cell:
	# Cell on the board 
	# Properties: 'image' and etc..
	# Add properties of cell here!
	def __init__(self, image):
		self.offset = 0.0
		self.image = monsters

	def tick(self, dt):
	 	self.offset = max(0.0, self.offset - dt * refillspeed)

class board:
	# A rectangular board of cells
	# Properties: width, height, size and etc...
	def __init__(self, width, height):
		self.width = boardwidth
		self.height = boardheight
		self.size = boardheight * boardwidth
		self.board = [cell(self.blank) for _ in range(self.size)]
		self.monsters = monsters
		self.background = background
		self.blank = blank
		self.matches = []
		self.refill = []
		self.score = 0.0

	def randomize(self):
		for i in range(self.size):
			self.board[j] = cell(random.choice(self.monsters))

	def busy(self):
		# If the board is busy animating a refill or sth, refuse swaps
		return self.refill or self.matches

	def pos(self, i, j):
		# Index of cell positions
		if (0 <= i < self.width) and (0 <= j < self.height):
			return j * self.width + i
		return None

	def tick(self, dt):
		if self.refill:
			for c in self.refill:
				c.tick(dt)
			self.refill = [c for c in self.refill if c.offset > 0]
			if self.refill:
				return
		elif self.matches:
			self.updatematch(self.blank)
			self.refill = list(self.refill())
		self.matches = self.findmatch()
		# self.score += score()

	def draw(self, display):
		display.blit(self.background, (0, 0))
		for i, c in enumerate(self.board):
			display.blit(c.image, (20, 160))

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
				c.image = random.choice(self.monsters)
				c.offset = offset
				yield c




class Game:
	# State of the game
	# Propteries: clock, display, font, board, score and etc..
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Little Monsters')
		self.screen = pygame.display.set_mode(size)
		self.board_size = board(columns, rows)
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

	def start(self):
		self.board.randomize()
		self.cursosr = [0, 0]
		self.score = 0.0
		self.swap_time = 20.0

	def quit(self):
		pygame.quit()
		sys.exit()

	def play(self):
		self.start()
		while True:
			self.draw()
			dt = min(self.clock.tick(fps) / 1000.0, 1.0 / fps)
			self.swap_time += dt
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit()
			self.board.tick(dt)
		

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


	def drawscore(self):
		t = self.score + self.board.scire
		text = self.font.render('Score: {}'.format(t), True, black)
		sreen.blit(text, (20,20))

	# def fill_monsters(self, board):

	# 	for x in range(boardwidth):
	# 		column_monsters = []
	# 		for y in range(boardheight):
	# 			if self.board[x][y] = empty_space:
	# 				column_monsters.append(board[x][y])
	# 		self.board[x] = ([empty_space] * (boardheight - len(column_monsters))) + column_monsters


	# def get_gem(self, board, x, y):
	# 	if  x >= boardwidth and y >= boardheight:
	# 		return None
	# 	else:
	# 		return board[x][y]


	# def drop_slots(self, board):
	# 	'''
	# 	Finds the slots in each column to put the monsters
	# 	'''
	# 	board_copy = copy.deepcopy(self.board)
	# 	# then we need to put down all gems
	# 	dropSlots = []
	# 	for x in range(boardwidth):
	# 		dropSlots.append([])
	# 		for y in range(boardheight - 1, -1, -1): # start from bottom and move up
	# 			if board_copy[x][y] == empty_space:
	# 				pos_monsters = list(range(len(monsters)))
	# 				for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
	# 					neighbor = get_gem(board_copy, x + offsetX, y + offsetY)
	# 					# need to make a get_gem function
	# 					if neighbor != None and neighbor in pos_monsters:
	# 						pos_monsters.remove(neighbor)
	# 				new_monster = random.choice(pos_monsters)
	# 				board_copy[x][y] = new_monster
	# 				dropSlots[x].append(new_monster)
	# 	return dropSlots


# To do list!!!
# Define Time
# Define Gem match
# Define Gem Disappear
# Define Gem drop down

if __name__ == "__main__":
	# for i in range(start_x, end_x, 60):
	# 	pygame.draw.line(screen, black, [i, start_y], [i, end_y])
	# 	screen.fill(monsters)
	# 	for j in range(start_y, end_y, 60):
	# 		pygame.draw.line(screen, black, [start_x, j], [end_x, j])



