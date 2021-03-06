from settings import *

import pygame
import os

from pygame.draw import *


class Objects():
	'''
	@ Абстрактный класс. У всех объектов должны быть определены координаты.
	'''
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_coords(self):
		return self.x, self.y

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def dx(self, dx):
		self.x += dx

	def dy(self, dy):
		self.y += dy
		

class StaticObjects(Objects):
	'''
	@ Класс статичных объектов. Нужен чтобы уметь различать мобов/героев от стен и прочих объектов
	'''
	def is_in(self, x, y):
		return (self.x <= x <= self.x + CELL_SIZE) and (self.y <= y <= self.y + CELL_SIZE)


class LiveObjects(Objects):
	'''
	@ Класс мобов/героев. Нужен чтобы уметь различать мобов/героев от стен и прочих объектов
	'''
	pass


class Space():
	'''
	@ Класс прстранства. Нужен чтобы реализовывать взаимодействие live_objects и static_objects
	'''
	def __init__(self, nps, mymap):
		self.nps = nps
		self.map = mymap

	def get_hero(self):
		for live in self.nps:
			if type(live) == type(Hero(0, 0)):
				return live

	def get_map(self):
		return self.map		


class Map():
	'''
	@ Класс карты, просто хранит static_objects. Нужен чтобы легко проверять на коллизии
	'''
	def __init__(self, static_objects):
		self.static_objects = static_objects
		self.exit = self.get_exit()

	def check_collision(self, x, y):
		for obj in self.static_objects:
			if obj != self.exit:
				if obj.is_in(x, y):
					return True
		return False

	def get_object(self, x, y):
		for obj in self.static_objects:
			if obj.is_in(x, y):
				return obj
		return 'empty'

	def get_exit(self):
		for obj in self.static_objects:
			if type(obj) == type(Exit(0, 0)):
				return obj


class Wall(StaticObjects):
	'''
	@ Класс стен
	'''
	pass


class Exit(StaticObjects):
	pass


class Hero(LiveObjects):
	'''
	@ Класс ГГ
	'''
	def set_angle(self, angle):
		self.angle = angle 

	def get_angle(self):
		return self.angle

	def rotate(self, dfi):
		self.angle += dfi


class Ray(Objects):
	'''
	@ Класс лучей
	@ Луч измеряет расстояние и может сказать объект в который врезался
	'''
	def __init__(self, x, y, angle, space):
		super().__init__(x,y)
		self.angle = angle
		self.map = space.get_map()
		self.collision_coords = (0, 0)
		self.r = self.measure_distance()

	def set_angle(self, angle):
		self.angle = angle

	def rotate(self, dfi):
		self.measure_distance()
		self.angle += dfi

	def get_angle(self):
		return self.angle

	def get_distance(self):
		return self.r

	def collided_object(self):
		return self.map.get_object(self.collision_coords[0], self.collision_coords[0])

	def measure_distance(self):
		self.r = 0
		dr = 1
		x0 = self.get_x()
		y0 = self.get_y()

		while self.r < MAX_DEPTH:
			x = x0 + self.r * math.cos(self.angle)
			y = y0 + self.r * math.sin(self.angle)
			if self.map.check_collision(x, y):
				self.collision_coords = (x, y)
				self._exact_distance()
				break

			self.r += dr

		return self.r

	def _exact_distance(self):
		dr = 0.1
		x0 = self.get_x()
		y0 = self.get_y()
		
		for i in range(10):
			x = x0 + self.r * math.cos(self.angle)
			y = y0 + self.r * math.sin(self.angle)
			if not self.map.check_collision(x, y):
				break
			self.r -= dr
		
		if not self.r:
			self.r = 0


class Camera(Objects):
	'''
	@ класс Камеры 
	@ пускает лучи и возращает холст
	'''
	def __init__(self, space):
		super().__init__(space.get_hero().get_x(), space.get_hero().get_y())
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.hero = space.get_hero()
		self.space = space
		
	def render(self):
		start_angle = self.space.get_hero().get_angle() + VIEW_ANGLE
		dfi = VIEW_ANGLE * 2 / DETALIZATION_DEGREE
		ray = Ray(self.hero.get_x(), self.hero.get_y(), start_angle, self.space)

		for i in range(DETALIZATION_DEGREE):
			self._paint_strip(i, ray.get_distance())
			ray.rotate(-dfi)

		return self.screen

	def _paint_strip(self, part_of_window, r):
		h_on_window = self._calc_h_on_window(r)
		color = self._get_color(r)

		x_on_window = WINDOW_WIDTH * part_of_window / DETALIZATION_DEGREE
		dx = WINDOW_WIDTH / DETALIZATION_DEGREE

		rct = pygame.Rect(x_on_window, WINDOW_HEIGHT / 2 - int(h_on_window / 2), dx, int(h_on_window))
		rect(self.screen, color, rct)

	def _calc_h_on_window(self, r):
		if r > 1:
			return WINDOW_HEIGHT / r
		else:
			return WINDOW_HEIGHT

	def _get_color(self, r):
		return [value * self._calc_brightness(r) for value in (255, 255, 255)]

	def _calc_brightness(self, r):
		if r > 2:
			return 0.5 + 2 / r ** 2
		else:
			return 1


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