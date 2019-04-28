# Game sounds
# 1 for background; 2 for swipe; 3 for combo; 4 for wrong; 5 for clock 
sounds = []
for i in range(1, 6):
	sounds.append(pygame.mixer.music.load('Sound%s.wav' % i))