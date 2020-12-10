import os

import pygame
from pygame.draw import *

from settings import *

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
	pass


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

	def check_collision(self, x, y):
		for obj in self.static_objects:
			if obj.is_in(x, y):
				return True
		return False

	def get_object(self, x, y):
		for obj in self.static_objects:
			if obj.is_in(x, y):
				return obj
		return 'empty'


class Wall(StaticObjects):
	'''
	@ Класс стен
	'''
	def is_in(self, x, y):
		return (self.x < x < self.x + CELL_SIZE) and (self.y < y < self.y + CELL_SIZE)


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


class LevelGenerator():
	'''
	@ Класс генератора уровней. Нужен чтоб брать на вход номер уровня и создавать Space().
	@ Карты хранятся в текстовом формате
	'''
	def __init__(self):
		self.legend = self.get_legend()

	def get_legend(self):
		legend = dict()
		data = self._get_data_from('legend')
		
		for line in data:
			char = line.split()[0]
			object_name = line.split()[-1]
			legend[char] = object_name

		return legend

	def generate_level(self, num_of_level):
		live_objects = []
		static_objects = []
		
		name_of_file = 'level' + str(num_of_level)
		raw_map = self._get_data_from(name_of_file)

		for y in range(len(raw_map)):
			for x in range(len(raw_map[0])):
				coords = (x * CELL_SIZE, y * CELL_SIZE)

				ch = raw_map[y][x]
				obj_name = self.legend[ch][:-2]

				if obj_name == 'Empty':
					continue

				tmp = []
				eval('tmp.append(' + obj_name + '(' + ','.join([str(coords[0]), str(coords[1])]) + '))') 
				tmp = tmp[0]

				if self._isLive(tmp):
					live_objects.append(tmp)
				else:
					static_objects.append(tmp)

		return Space(live_objects, Map(static_objects))

	def _isLive(self, obj):
		objectType = type(obj)
		return 'LiveObjects' in str(objectType.__bases__)

	def _get_data_from(self, name_of_file):
		path = os.path.join(PATH_TO_LEVELS, name_of_file)
		if not path.endswith('.txt'):
			path += '.txt' 
		
		data = []
		with open(path, 'r') as f:
			data = [line.strip() for line in f]

		return data


class Ray(Objects):
	def __init__(self, x, y, angle, space):
		super().__init__(x,y)
		self.angle = angle
		self.map = space.get_map()
		self.collision_coords = (0, 0)

	def measure_distance(self):
		r = 0
		dr = 0.1
		x0 = self.get_x()
		y0 = self.get_y()

		while r < MAX_DEPTH:
			x = float(x0 + r * math.cos(self.angle))
			y = float(y0 + r * math.sin(self.angle))
			
			if self.map.check_collision(x, y):
				self.collision_coords = (x, y)
				break

			r += dr
		return float(r)

	def set_angle(self, angle):
		self.angle = angle

	def rotate(self, dfi):
		self.angle += dfi

	def get_angle(self):
		return self.angle

	def collided_object(self):
		return self.map.get_object(self.collision_coords[0], self.collision_coords[0])


class Camera(Objects):
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
			self._paint_strip(i, ray.measure_distance())
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


class EventProcessor():
	def __init__(self, space):
		self.space = space
		self.hero = space.get_hero()
		self.angle_speed = 0
		self.dx = self.dy = 0

	def mousemotion(self, pos):
		x = pos[0]
		if abs((x - WINDOW_WIDTH/2) / (WINDOW_WIDTH / 2)) > SENSE:
			self.angle_speed = - ANGLE_SPEED * (x - WINDOW_WIDTH/2) / (WINDOW_WIDTH / 2)
		else:
			self.angle_speed = 0

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

	def is_empty(self):
		return not self.space.map.check_collision(self.hero.get_x() + self.dx, self.hero.get_y() + self.dy)

	def stop(self):
		self.dx = 0
		self.dy = 0

	def stoprotation(self):
		self.angle_speed = 0