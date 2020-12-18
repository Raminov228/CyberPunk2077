from settings import *
import random
import os

class LabirintGenerator():
	'''
	@ Генератор лабиринта
	@ Выдает txt файл с лабиринтом
	'''
	def __init__(self):
		self.labirint_map = [['#' for _ in range(LABIRINT_SIZE[0])] for a in range(LABIRINT_SIZE[1])]
		
		for y in range(LABIRINT_SIZE[1]):
			for x in range(LABIRINT_SIZE[0]):
				if 1 <= x < LABIRINT_SIZE[0] - 1 and 1 <= y < LABIRINT_SIZE[1] - 1 :
					self.labirint_map[y][x] = '0'

		for y in range(LABIRINT_SIZE[1]):
			for x in range(LABIRINT_SIZE[0]):
				if x % 2 and y % 2:
					self.labirint_map[y][x] = '.'

		self.labirint_map[1][1] = '*'

	def generate_labirint(self):
		l = self.generate_random_l()
		x, y = 1, 1
		while x != LABIRINT_SIZE[0] - 2 or y != LABIRINT_SIZE[1] - 2:
			if self.is_in(x + l[0], y + l[1]):
				x += l[0]
				y += l[1]
				self.make_empty(x, y)
				x += l[0]
				y += l[1]
				self.make_empty(x, y)
			l = self.generate_random_l()
		
		for y in range(LABIRINT_SIZE[1]):
			for x in range(LABIRINT_SIZE[0]):
				if self.labirint_map[y][x] == '0':
					self.labirint_map[y][x] = '#'
		
		self.labirint_map[1][1] = '*'
		self.labirint_map[LABIRINT_SIZE[1] - 1][LABIRINT_SIZE[0] - 2] = 'e'
		return self.labirint_map

	def make_empty(self, x, y):
		self.labirint_map[y][x] = '.'

	def generate_random_l(self):
		all_l = [[0, 1], [0, -1], [1, 0], [-1, 0]]
		return all_l[random.randint(0, 3)]

	def is_in(self, x, y):
		return 1 <= x <= LABIRINT_SIZE[0] - 2 and 1 <= y <= LABIRINT_SIZE[1] - 2

	def generate_txt(self):
		lab = self.generate_labirint()
		text = '\n'.join([''.join(line) for line in lab])
		
		with open(self._get_path('level0'), 'w') as f:
			f.write(text)

	def _get_path(self, name_of_file):
		path = os.path.join(PATH_TO_LEVELS, name_of_file)
		if not path.endswith('.txt'):
			path += '.txt' 
		
		return path