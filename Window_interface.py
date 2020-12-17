from settings import *

import pygame
from pygame.draw import *

class Button():
	def __init__(self, coords, size, color):
		self.x, self.y = coords
		self.size = size
		self.is_clicked = False
		self.color = color

	def is_in(self, pos):
		x = pos[0]
		y = pos[1]
		return self.x <= x <= self.x + self.size[0] and self.y <= y <= self.y + self.size[1]

	def click(self, pos):
		if self.is_in(pos):
			self.is_clicked = True

	def get_state(self):
		return self.is_clicked


class Menu():
	def __init__(self):
		self.finished = False
		self.quit = False

		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		
		self.start_button = Button(START_BUTTON_COORDS, START_BUTTON_SIZE, START_BUTTON_COLOR) 
		self.exit_button = Button(EXIT_BUTTON_COORDS, EXIT_BUTTON_SIZE, EXIT_BUTTON_COLOR)

		self.buttons = {'start': self.start_button, 'exit': self.exit_button}

	def render(self):
		self.screen.fill((0, 0, 0))
	
		self.finished = self.start_button.get_state()
		self.quit = self.exit_button.get_state()

		for key in self.buttons:
			button = self.buttons[key]
			rct = pygame.Rect(button.x, button.y, button.size[0], button.size[1])
			rect(self.screen, button.color, rct)
			
			pygame.font.init()
			
			f1 = pygame.font.Font(None, 36)
			text1 = f1.render(key, True, (255, 255, 255))
 
			self.screen.blit(text1, (button.x + 10, button.y + 10))

		return self.screen


class MenuProcessor():
	def __init__(self, menu):
		self.buttons = menu.buttons

	def click_parcer(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for key in self.buttons:
					button = self.buttons[key]
					button.click(event.pos)

	def update(self):
		return self.buttons['start'].get_state(), self.buttons['exit'].get_state() 