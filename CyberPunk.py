MAX_DEPTH = 100
CELL_SIZE = 10
PATH_TO_LEVELS = 'levels'

import os

class Objects():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get_coords():
		return self.x, self.y


class StaticObjects(Objects):
	pass


class LiveObjects(Objects):
	pass


class Space():
	def __init__(self, nps, mymap):
		self.nps = nps
		self.map = mymap


class Map():
	def __init__(self, static_objects):
		self.static_objects = static_objects


class Wall(StaticObjects):
	def is_in(self, x, y):
		return (self.x <= x <= self.x + CELL_SIZE) and (self.y <= x <= self.y + CELL_SIZE)


class Hero(LiveObjects):
	pass


class LevelGenerator():
	def __init__(self):
		self.legend = self.get_legend

	def get_legend(self):
		legend = dict()
		data = self._get_data_from('legend')
		
		for line in data:
			char = line.split()[0]
			object_name = line.split()[-1]
			legend[char] = object_name

		return legend

	def generate_level(num_of_level):
		live_objects = []
		static_objects = []
		return Space(live_objects, Map(static_objects))


	def _get_data_from(self, name_of_file):
		path = os.path.join(PATH_TO_LEVELS, name_of_file)
		if not path.endwith('.txt'):
			path += '.txt' 
		
		data = []
		with open(path, 'r') as f:
			data = [line.strip() for line in f]

		return data


generator = LevelGenerator()
space = generator.generate_level(1)
print(generator.get_legend())
