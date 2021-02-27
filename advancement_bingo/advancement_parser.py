import os
import json

class Advancement:
	def __init__(self, difficulty, filename):
		self.difficulty = difficulty
		self.filename = filename

	@property
	def id(self):
		return os.path.join(self.difficulty, self.filename)

	def get_file_handle(self):
		return open(self.path, 'r')

	def get_data(self):
		return json.load(self.get_file_handle())

	@property
	def path(self):
		return os.path.join('advancements', self.difficulty, self.filename)
	

all_advancements = []

for difficulty_level in os.listdir('advancements'):
	filenames = os.listdir(os.path.join('advancements', difficulty_level))
	for filename in filenames:
		all_advancements.append(Advancement(difficulty=difficulty_level, filename=filename))

item_png_map = {}


def load_item_map():
	f = open('items_textures.json', 'r')
	data = json.load(f)
	for item in data:
		if item["texture"]:
			folder, name = item["texture"].split('/')
			png = os.path.join(folder + 's', name + '.png')
			item_png_map[f'minecraft:{item["name"]}'] = png

load_item_map()

serialized_advancements = []

for adv in all_advancements:
	data = adv.get_data()
	advancement = {}
	advancement['id'] = adv.id
	advancement['difficulty_level'] = adv.difficulty
	advancement['title'] = data['display']['title']
	advancement['description'] = data['display']['description']
	png = item_png_map[data['display']['icon']['item']]
	advancement['icon'] = png
	serialized_advancements.append(advancement)
