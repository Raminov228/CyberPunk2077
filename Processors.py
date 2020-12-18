from settings import *
import pygame

class MainProcessor():
	'''
	@ Процессор обрабатывающий нажатия во время игры
	'''
	def __init__(self, space):
		self.space = space
		self.hero = space.get_hero()
		self.angle_speed = 0
		self.dx = self.dy = 0
		self.exit = space.map.get_exit()

	def mousemotion(self, pos):
		x = pos[0]
		if abs((x - WINDOW_WIDTH/2) / (WINDOW_WIDTH / 2)) > SENSE:
			self.angle_speed = - ANGLE_SPEED * (x - WINDOW_WIDTH/2) / (WINDOW_WIDTH / 2)
		else:
			self.angle_speed = 0

	def key_parcer(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				self.forward()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				self.backward()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				self.right()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				self.left()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				self.stop()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_s:
				self.stop()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				self.stop()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				self.stop()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_e:
				self.rotateright()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_e:
				self.stoprotation()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				self.rotateleft()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_q:
				self.stoprotation()

	def rotateright(self):
		self.angle_speed = -ANGLE_SPEED

	def rotateleft(self):
		self.angle_speed = ANGLE_SPEED		

	def forward(self):
		self.dx = SPEED * math.cos(self.hero.get_angle())
		self.dy = SPEED * math.sin(self.hero.get_angle())

	def backward(self):
		self.dx = - SPEED * math.cos(self.hero.get_angle())
		self.dy = - SPEED * math.sin(self.hero.get_angle())

	def right(self):
		self.dx = SPEED * math.cos(self.hero.get_angle() - math.pi / 2)
		self.dy = SPEED * math.sin(self.hero.get_angle() - math.pi / 2)
		
	def left(self):
		self.dx = SPEED * math.cos(self.hero.get_angle() + math.pi / 2)
		self.dy = SPEED * math.sin(self.hero.get_angle() + math.pi / 2)
		
	def update(self):
		self.hero.rotate(self.angle_speed)
		if (self.dx or self.dx) and self.is_empty():
			self.hero.dx(self.dx)
			self.hero.dy(self.dy)

		return self.is_exit()

	def is_exit(self):
		return self.exit.is_in(self.hero.get_x(), self.hero.get_y())

	def is_empty(self):
		return not self.space.map.check_collision(self.hero.get_x() + self.dx, self.hero.get_y() + self.dy)


	def stop(self):
		self.dx = 0
		self.dy = 0

	def stoprotation(self):
		self.angle_speed = 0


class MenuProcessor():
	'''
	@ Класс процессора меню (обрабатывает нажатия)
	'''
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