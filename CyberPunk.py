import pygame
from pygame.draw import *

#импортим все объекты
from objects import *

import os
 
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

FPS = 30
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

generator = LevelGenerator()
space = generator.generate_level(1)
hero = space.get_hero()
hero.set_angle(math.pi / 2)

cam = Camera(space)
screen.blit(cam.render(), (0, 0))

procc = EventProcessor(space)

pygame.display.update()
clock = pygame.time.Clock()
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
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				procc.forward()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				procc.backward()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				procc.right()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				procc.left()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				procc.stop()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_s:
				procc.stop()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				procc.stop()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				procc.stop()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_e:
				procc.rotateright()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_e:
				procc.stoprotation()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				procc.rotateleft()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_q:
				procc.stoprotation()		


	rect(screen, (0, 0, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT / 2))
	rect(screen, (0, 255, 0), (0, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT / 2))

	screen.blit(cam.render(), (0, 0))
	procc.update()
	pygame.display.update()

pygame.quit()