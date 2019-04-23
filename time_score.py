'''
This file serves to create the clock and the scoreboard
for our final project game. 
'''
import random, time, pygame, sys
from pygame.locals import *

board_width = 4
board_height = 4
empty_space = -1 
window_width = 600
window_height = 600 


def main():
    global clock, display_game

    # Initial set up of clock
    pygame.init()
    font = pygame.font.Font(None,72)
    display_game = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Little Monsters")
    clock = pygame.time.Clock() 
    basic_font = pygame.font.Font('freesansbold.ttf', 36)
  
'''
    while True:
    	clock.tick(40)
    	# indicates 40 frames per second
    	
    	# pygame.display.update()

    	


def run_game():
	# initialize the board
	# drop initial monsters

    gameBoard = getBlankBoard() # need this function
    score = 0
    fillBoardAndAnimate(gameBoard, [], score) # need this function
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

    	score_add = 0
    	while matched_gems != []:
    		points = []
    		for gemMatch in matched_gems:
    			if len(gemMatch) == 3:
    				scoreAdd += 3
    			if len(gemMatch) == 4:
    				scoreAdd += 5
    			if len(gemMatch) == 5:
    				scoreAdd += 10
    		points.append(scoreAdd)
    		score += scoreAdd

def blank_board():
	board = []
	for x in range(board_with):
		board.append([empty_space] * board_height)
	return board

def fill_board():
'''

if __name__ == "__main__":
	main()

	



