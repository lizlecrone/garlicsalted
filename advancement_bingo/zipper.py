import os
import random
import zipfile

all_advancements = os.listdir('advancements')

def advancement_function(number):
	return (
		'scoreboard players add @s points 1\n'
		f'execute if score @s points matches {number} run function hunt:gameover'
	)

def write(archive, filepath, destination):
	archive.write(filepath, os.path.join(destination, filepath))

def generate_random_zip(fp):
	selected_advancements = random.sample(all_advancements, 5)
	generate_zip(fp, selected_advancements)

def generate_zip(fp, selected_advancements):
	
	with zipfile.ZipFile(fp, 'w') as archive:
		top_folder = 'hunt'
		data_folder = os.path.join(top_folder, 'data')
		hunt_folder = os.path.join(data_folder, 'hunt')
		advancements_folder = os.path.join(hunt_folder, 'advancements')
		write(archive, 'pack.mcmeta', top_folder)
		for function in os.listdir('functions'):
			write(archive, os.path.join('functions', function), hunt_folder)
		archive.writestr(
			os.path.join(hunt_folder, 'functions', 'advancement.mcfunction'),
			advancement_function(len(selected_advancements))
		)
		write(archive, 'root.json', advancements_folder)
		for advancement in selected_advancements:
			write(archive, os.path.join('advancements', advancement), hunt_folder)