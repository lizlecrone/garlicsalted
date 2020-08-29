import os
import json

all_advancement_files = os.listdir('advancements')

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

advancements = []

for file in all_advancement_files:
	file_handle = open(os.path.join('advancements', file), 'r')
	data = json.load(file_handle)
	advancement = {}
	advancement['id'] = file
	advancement['title'] = data['display']['title']
	advancement['description'] = data['display']['description']
	png = item_png_map[data['display']['icon']['item']]
	advancement['icon'] = png
	advancements.append(advancement)
