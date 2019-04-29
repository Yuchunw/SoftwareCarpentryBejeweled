import pygame, random, time, sys
from pygame.locals import *
import itertools
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

monster_width = 50               # Width of each shape (pixels).
monster_height = 50              # Height of each shape (pixels).
game_columns = 8              # Number of columns on the board.
game_rows = 8               # Number of rows on the board.
margin = 50                      # margin around the board (pixels).
disp_width = game_columns * monster_width + 2 * margin
disp_height = game_rows * monster_height + 2 * margin + 150
font_size = 36
text_offset = margin + 5

# Map from number of matches to points scored.
score_points = {0: 0, 1: .9, 2: 3, 3: 9, 4: 27}
min_match = 3
extra_points = .1
random_points = .3
DELAY_PENALTY_SECONDS = 10
DELAY_PENALTY_POINTS = .5

FPS = 30
explosion_time = 15            # In frames per second.
refill_time = 10               # In cells per second.

background_image = pygame.image.load("Gameboard.png")

# # Game sounds
# # 1 for background; 2 for swipe; 3 for combo; 4 for wrong; 5 for clock 
pygame.mixer.init()
Sounds = []
for i in range(1, 6):
    Sounds.append(pygame.mixer.Sound('Sound%s.wav' % i))


class Cell(object):
    """
    A cell on the board, with properties:
    `image` -- a `Surface` object containing the sprite to draw here.
    `offset` -- vertical offset in pixels for drawing this cell.
    """
    def __init__(self, image):
        self.offset = 0.0
        self.image = image

    def tick(self, dt):
        self.offset = max(0.0, self.offset - dt * refill_time)

class Board(object):
    """
    A rectangular board of cells, with properties:
    `w` -- width in cells.
    `h` -- height in cells.
    `size` -- total number of cells.
    `board` -- list of cells.
    `matches` -- list of matches, each being a list of exploding cells.
    `refill` -- list of cells that are moving up to refill the board.
    `score` -- score due to chain reactions.
    """
    def __init__(self, width, height):
    	images = []
    	for i in range(1, 6):
        	monster_image = pygame.image.load('Monster%s.png' % i)
        	if monster_image.get_size() != (monster_width, monster_height):
           		monster_image = pygame.transform.smoothscale(monster_image, (monster_width, monster_height))
        	images.append(monster_image)

        self.shapes = images
        self.explosion = [pygame.image.load('star{}.png'.format(i)) for i in range(1, 7)]
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
        """
        Replace the entire board with fresh shapes.
        """
        for i in range(self.size):
            self.board[i] = Cell(random.choice(self.shapes))

    def pos(self, i, j):
        """
        Return the index of the cell at position (i, j).
        """
        assert(0 <= i < self.w)
        assert(0 <= j < self.h)
        return j * self.w + i

    def busy(self):
        """
        Return `True` if the board is busy animating an explosion or a
        refill and so no further swaps should be permitted.
        """
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
        """
        Draw the board on the pygame surface `display`.
        """
        display.blit(self.background, (0, 0))
        for i, c in enumerate(self.board):
            display.blit(c.image,
                         (50 + monster_width * (i % self.w),
                          200 + monster_height * (i // self.w - c.offset)))

    def swap(self, cursor):
        """
        Swap the two board cells covered by `cursor` and update the
        matches.
        """
        i = self.pos(*cursor)
        b = self.board
        b[i], b[i+1] = b[i+1], b[i]
        self.matches = self.find_matches()
        Sounds[1].play()

    def find_matches(self):
        """
        Search for matches (lines of cells with identical images) and
        return a list of them, each match being represented as a list
        of board positions.
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
        """
        Replace all the cells in any of the matches with `image`.
        """
        for match in self.matches:
            for position in match:
                self.board[position].image = image

    def refill_columns(self):
        """
        Move cells downwards in columns to fill blank cells, and
        create new cells as necessary so that each column is full. Set
        appropriate offsets for the cells to animate into place.
        """
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
    """
    The state of the game, with properties:
    `clock` -- the pygame clock.
    `display` -- the window to draw into.
    `font` -- a font for drawing the score.
    `board` -- the board of cells.
    `cursor` -- the current position of the (left half of) the cursor.
    `score` -- the player's score.
    `last_swap_ticks` -- 
    `swap_time` -- time since last swap (in seconds).
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Little Monsters")
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((disp_width, disp_height))
        self.board = Board(game_columns, game_rows)
        self.font = pygame.font.Font(None, font_size)

    def start(self):
        """
        Start a new game with a random board.
        """
        self.board.randomize()
        self.cursor = [0, 0]
        self.score = 0.0
        self.swap_time = 0.0

    def quit(self):
        """
        Quit the game and exit the program.
        """
        pygame.quit()
        sys.exit()

    def play(self):
        """
        Play a game: repeatedly tick, draw and respond to input until
        the QUIT event is received.
        """
        self.start()
        while True:
            self.draw()
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)
            self.swap_time += dt
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
    	swap_penalties = int(self.swap_time / DELAY_PENALTY_SECONDS)
    	self.swap_time = 0.0
        if match(self.cursor) == True:
    	   self.board.swap(self.cursor)

    	self.score -= 1 + DELAY_PENALTY_POINTS * swap_penalties
    	self.score += score_points[len(self.board.matches)]
    	for match in self.board.matches:
    		self.score += (len(match) - min_match) * extra_points

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









