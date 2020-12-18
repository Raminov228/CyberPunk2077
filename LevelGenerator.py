from settings import *

import objects
import os


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
				coords = [x * CELL_SIZE, y * CELL_SIZE]
				ch = raw_map[y][x]
				obj_name = self.legend[ch][:-2]

				if obj_name == 'Empty':
					continue

				if obj_name == 'Hero':
					coords[0] = CELL_SIZE + CELL_SIZE / 2
					coords[1] = CELL_SIZE + CELL_SIZE / 2

				tmp = []
				eval('tmp.append(' + 'objects.'+ obj_name + '(' + ','.join([str(coords[0]), str(coords[1])]) + '))') 
				tmp = tmp[0]

				if self._isLive(tmp):
					live_objects.append(tmp)
				else:
					static_objects.append(tmp)

		return objects.Space(live_objects, objects.Map(static_objects))

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