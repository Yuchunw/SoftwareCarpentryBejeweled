
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
