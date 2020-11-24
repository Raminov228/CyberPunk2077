import os

#просто вынес константы в отдельный файл
from settings import *


class Objects():
	'''
	@ Абстрактный класс. У всех объектов должны быть определены координаты.
	'''
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_coords():
		return self.x, self.y


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


class Map():
	'''
	@ Класс карты, просто хранит static_objects. Нужен чтобы легко проверять на коллизии
	'''
	def __init__(self, static_objects):
		self.static_objects = static_objects


class Wall(StaticObjects):
	'''
	@ Класс стен
	'''
	def is_in(self, x, y):
		return (self.x <= x <= self.x + CELL_SIZE) and (self.y <= y <= self.y + CELL_SIZE)


class Hero(LiveObjects):
	'''
	@ Класс ГГ
	'''
	pass


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


generator = LevelGenerator()
space = generator.generate_level(1)

print(space.nps)
print(space.map)

hero = space.get_hero()
print(hero.x)
print(hero.y)