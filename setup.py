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

# Parameters for Draw board on screen
boardwidth = 480
boardheight = 480
black = (0, 0, 0)
start_x = 23
start_y = 218
end_x = start_x + boardwidth
end_y = start_y + boardheight
columns = 8
rows = 8

# Set up cells
monster1 = pygame.image.load('Monster1.png').convert()
monster2 = pygame.image.load('Monster2.png').convert()
monster3 = pygame.image.load('Monster3.png').convert()
monster4 = pygame.image.load('Monster4.png').convert()
monster5 = pygame.image.load('Monster5.png').convert()

monsters = {0: 'monster1', 1: 'monster2', 2: 'monster3' , 3: 'monster4', 4: 'monster5'}

# Rules for Game
matchmin = 3

# Loop until the user clicks the close button
done = False

while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	# Blit background image
	screen.blit(background_image, (0, 0))
	
	# Draw the grid
	for i in range(start_x, end_x + 1, 60):
		pygame.draw.line(screen, black, [i, start_y], [i, end_y])
	for j in range(start_y, end_y + 1, 60):
		pygame.draw.line(screen, black, [start_x, j], [end_x, j])

	# Update the screen 
	pygame.display.flip()

	# Limite to 60 frames per second
	clock.tick(60)
