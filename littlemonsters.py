"""
This is a bejewelled like game made for our final project in
Software Carpentry. The game is called "Little Monsters." 
Authors: Joan Golding, Sicong, and Yuchun Wang 
Date: 4/29/2019
"""

import pygame, random, time, sys
from pygame.locals import *
import itertools
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

monster_width = 50
monster_height = 50
game_columns = 8
game_rows = 8
margin = 50
disp_width = game_columns * monster_width + 2 * margin
disp_height = game_rows * monster_height + 2 * margin + 150
font_size = 36
text_offset = margin + 5

score_points = {0: 0, 1: 0.9, 2: 3, 3: 9, 4: 27}
min_match = 3
extra_points = 0.1
random_points = .3


FPS = 30
explosion_time = 15 
refill_time = 10

background_image = pygame.image.load("Gameboard.png")
game_over_image = pygame.image.load("Gameover.png")

pygame.mixer.init()
Sounds = []
for i in range(1, 6):
	Sounds.append(pygame.mixer.Sound('Sound%s.wav' % i))


class Cell(object):
	def __init__(self, image):
		self.offset = 0.0
		self.image = image
	def tick(self, dt):
		self.offset = max(0.0, self.offset - dt * refill_time)

class Board(object):
	def __init__(self, width, height):
		images = []
		for i in range(1, 6):
			monster_image = pygame.image.load('Monster%s.png' % i)
			if monster_image.get_size() != (monster_width, monster_height):
				monster_image = pygame.transform.smoothscale(monster_image, (monster_width, monster_height))
				images.append(monster_image)

		self.shapes = images
		self.explosion = [pygame.image.load('star{}.png'.format(i)) for i in range(1, 7)]
		# transform the background to fit the disp_width and disp_height
		self.background = pygame.transform.smoothscale(background_image, (disp_width, disp_height))
		self.blank = pygame.image.load("Gameboard.png")
		self.w = width
		self.h = height
		self.size = width * height
		self.board = [Cell(self.blank) for _ in range(self.size)]
		self.matches = []
		self.refill = []
		self.score = 0.0

	def randomize(self):
		for i in range(self.size):
			self.board[i] = Cell(random.choice(self.shapes))

	def pos(self, i, j):
		assert(0 <= i < self.w)
		assert(0 <= j < self.h)
		return j * self.w + i
	
	def busy(self):
		return self.refill or self.matches
	
	def tick(self, dt):
		if self.refill:
			for c in self.refill:
				c.tick(dt)
			self.refill = [c for c in self.refill if c.offset > 0]

		if self.refill:
			return
		elif self.matches:
			self.explosion_time += dt
			f = int(self.explosion_time * explosion_time)
			if f < len(self.explosion):
				self.update_matches(self.explosion[f])
				return
			self.update_matches(self.blank)
			self.refill = list(self.refill_columns())
		self.explosion_time = 0
		self.matches = self.find_matches()
		self.score += len(self.matches) * random_points

	def draw(self, display):
		display.blit(self.background, (0, 0))
		for i, c in enumerate(self.board):
			display.blit(c.image,
					(50 + monster_width * (i % self.w),
					200 + monster_height * (i // self.w - c.offset)))

	def swap(self, cursor):
		i = self.pos(*cursor)
		b = self.board
		b[i], b[i+1] = b[i+1], b[i]
		self.matches = self.find_matches()

	def find_matches(self):
		"""
		See if two pictures match.
		"""
		def lines():
			for j in range(self.h):
				yield range(j * self.w, (j + 1) * self.w)
			for i in range(self.w):
				yield range(i, self.size, self.w)
		def key(i):
			return self.board[i].image
		def matches():
			for line in lines():
				for _, group in itertools.groupby(line, key):
					match = list(group)
					if len(match) >= min_match:
						yield match
		return list(matches())

	def update_matches(self, image):
		for match in self.matches:
			for position in match:
				self.board[position].image = image

	def refill_columns(self):
		for i in range(self.w):
			target = self.size - i - 1
			for pos in range(target, -1, -self.w):
				if self.board[pos].image != self.blank:
					c = self.board[target]
					c.image = self.board[pos].image
					c.offset = (target - pos) // self.w
					target -= self.w
					yield c
			offset = 1 + (target - pos) // self.w
			for pos in range(target, -1, -self.w):
				c = self.board[pos]
				c.image = random.choice(self.shapes)
				c.offset = offset
				yield c

class Game(object):
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Little Monsters")
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((disp_width, disp_height))
		self.board = Board(game_columns, game_rows)
		self.font = pygame.font.Font('CantikaHandwriting.otf', font_size)

	def start(self):
		Sounds[0].play()
		self.board.randomize()
		self.cursor = [0, 0]
		self.score = 0.0
		self.swap_time = 20

	def quit(self):
		pygame.quit()
		sys.exit()

	def play(self):
		self.start()
		while True:
			self.draw()
			if self.swap_time != 0:
				dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
				self.swap_time -= dt
			else:
				self.swap_time = 0 
			for event in pygame.event.get():
				if event.type == KEYUP:
					self.input(event.key)
				elif event.type == QUIT:
					self.quit()

			self.board.tick(dt)

	def input(self, key):
		if key == K_q:
			self.quit()
		elif key == K_RIGHT and self.cursor[0] < self.board.w - 2:
			self.cursor[0] += 1
		elif key == K_LEFT and self.cursor[0] > 0:
			self.cursor[0] -= 1
		elif key == K_DOWN and self.cursor[1] < self.board.h - 1:
			self.cursor[1] += 1
		elif key == K_UP and self.cursor[1] > 0:
			self.cursor[1] -= 1
		elif key == K_SPACE and not self.board.busy():
			self.swap()

	def swap(self):
		self.swap_time += 5
		self.board.swap(self.cursor)
		self.score += score_points[len(self.board.matches)]
		for match in self.board.matches:
			self.score += (len(match) - min_match) * extra_points

			if len(match) >= min_match:
				Sounds[2].play()
	
	def draw(self):
		self.board.draw(self.display)
		self.draw_score()
		self.draw_time()
		self.draw_cursor()
		pygame.display.update()
	
	def draw_time(self):
		s = int(self.swap_time)
		text = self.font.render('{}:{:02}'.format(s / 60, s % 60),
								True, BLACK)
		self.display.blit(text, (400, 115))
		if s <= 5:
			Sounds[4].play()

		if s <= 0:
			self.display.blit(self.board.background, (0,0))
			self.display.blit(game_over_image, (100, 400))
	
	def draw_score(self):
		total_score = self.score + self.board.score
		text = self.font.render('{}'.format(total_score), True, BLACK)
		self.display.blit(text, (135, 115))

	def draw_cursor(self):
		topLeft = (50 + self.cursor[0] * monster_width,
				200 + self.cursor[1] * monster_height)
		topRight = (topLeft[0] + monster_width * 2, topLeft[1])
		bottomLeft = (topLeft[0], topLeft[1] + monster_height)
		bottomRight = (topRight[0], topRight[1] + monster_height)
		pygame.draw.lines(self.display, BLACK, True,
						[topLeft, topRight, bottomRight, bottomLeft], 3)

if __name__ == '__main__':
	Game().play()









