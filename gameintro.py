import pygame
import time

 
pygame.init()
 
display_width = 400
display_height = 534
 
black = (0,0,0)
white = (255,255,255)
green = (173,186,70)
lightgreen = (243,246,221)

Display = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
startmenu = pygame.image.load('Start.png')
 

def text_objects(text, font):
    textSurface = font.render(text, True, green)
    return textSurface, textSurface.get_rect()


def game_intro():
	'''
	This function shows players an start menu before the actual game
	'''
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        Display.fill(white)
        Display.blit(startmenu,(0,0))
        button("start",140,425,110,40,white,lightgreen,pygame.quit)
        #if we want to start the game, replace pygame.quit with game_loop or something
        pygame.display.update()
        clock.tick(15)


def button(msg,x,y,w,h,ic,ac,action=None):
	'''
	This function is a general button function.
	Parameters:
	msg: What do you want the button to say on it.
	x: The x location of the top left coordinate of the button box.
	y: The y location of the top left coordinate of the button box.
	w: Button width.
	h: Button height.
	ic: Inactive color (when a mouse is not hovering).
	ac: Active color (when a mouse is hovering).
	'''
	
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(Display, ac,(x,y,w,h))

		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(Display, ic,(x,y,w,h))
	pygame.font.init()
	smallText = pygame.font.Font('CantikaHandwriting.otf',50)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	Display.blit(textSurf, textRect)


game_intro()
