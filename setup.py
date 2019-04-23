# This code is used for setting up the game and load the background with the image
# Make sure the background file name matchs the code. 

# -*- coding: utf-8 -*-

import pygame

pygame.init()

# Set up the screen
size = (600, 750)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Little Monsters')

# To manage how fast the screen updates
clock = pygame.time.Clock()

# Load the background image
background_image = pygame.image.load('background.png').convert()

# Draw board on screen
boardwidth = 480
boardheight = 476
start_x = 23
start_y = 218
startpos = (start_x, start_y)
endpos = (start_x + boardwidth, start_y + boardheight)

Black = (0, 0, 0)
pygame.draw.line(screen, Black, startpos, endpos, width = 1)

# Loop until the user clicks the close button
done = False

while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	# Blit background image
	screen.blit(background_image, (0, 0))

	# Update the screen 
	pygame.display.flip()

	# Limite to 60 frames per second
	clock.tick(60)
