# This code is used for setting up the game and load the background with the image
# Make sure the background file name matchs the code. 

# -*- coding: utf-8 -*-

import pygame, random

pygame.init()

# Set up the screen
size = (400, 534)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Little Monsters')

# To manage how fast the screen updates
clock = pygame.time.Clock()
timer = 20
dt = 0

# Load the background image
background_image = pygame.image.load('Gameboard.png').convert()

# Parameters for Draw board on screen
boardwidth = 364
boardheight = 363
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

# Load the images
monsters = []
for i in range(1, 6):
	monster_image = pygame.image.load('Monster%s.png' % i)
	if monster_image.get_size() != (monster_size, monster_size):
		monster_image = pygame.transform.smoothscale(monster_image, (monster_size, monster_size))
	monsters.append(monster_image)

# Rules for Game
matchmin = 3

# Game sounds
# 1 for background; 2 for swipe; 3 for combo; 4 for wrong; 5 for clock 
sounds = []
for i in range(1, 6):
	sounds.append(pygame.mixer.music.load('Sound%s.wav' % i))

# Loop until the user clicks the close button
done = False

while not done:


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True


	# Blit background image
	screen.blit(background_image, (0, 0))

	timer -= 1
	if timer <= 0:
		timer = 20 

	text = font.render(str(timer), True, black)
	screen.blit(text, (320, 95))
	pygame.display.flip()
	# Limit to 60 frames per second
	clock.tick(1) 
	


	# Draw the grid
	for i in range(start_x, end_x, 60):
		pygame.draw.line(screen, black, [i, start_y], [i, end_y])
	for j in range(start_y, end_y, 60):
		pygame.draw.line(screen, black, [start_x, j], [end_x, j])


	
	# Update the screen 
	pygame.display.flip()


