import pygame
from pygame.draw import *

#импортим все объекты
from objects import *

from Window_interface import *

import os
 
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

FPS = 30

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

while 1:
	menu = Menu()
	menuprocc = MenuProcessor(menu)

	finished = False
	quit = False

	while not finished and not quit:
		clock.tick(FPS)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
			
			menuprocc.click_parcer(event)

		screen.blit(menu.render(), (0, 0))
		finished, quit = menuprocc.update()
		pygame.display.update()

	print(finished, quit)

	if quit:
		break


	generator = LevelGenerator()
	space = generator.generate_level(1)
	hero = space.get_hero()
	hero.set_angle(math.pi / 2)

	cam = Camera(space)
	screen.blit(cam.render(), (0, 0))

	procc = MainProcessor(space)

	pygame.display.update()

	finished = False

	pygame.mouse.set_pos([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2])
	colibrarion = False

	while not finished:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				finished = True
			
			if event.type == pygame.MOUSEMOTION:
				if colibrarion:
					procc.mousemotion(event.pos)
					colibrarion = False
				else:
					colibrarion = True
			
			procc.key_parcer(event)

		rect(screen, (0, 0, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT / 2))
		rect(screen, (0, 255, 0), (0, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT / 2))

		screen.blit(cam.render(), (0, 0))
		finished = procc.update()
		pygame.display.update()



pygame.quit()