import os
import random
import zipfile
from advancement_parser import all_advancements


def advancement_function(number):
    return (
        'scoreboard players add @s points 1\n'
        f'execute if score @s points matches {number} run function hunt:gameover'
    )

def series_advancement_function(order_number, best_of_number, total):
    if order_number == total:
        return(
            f'advancement revoke @a only hunt:dummy_{order_number}\n'
            'scoreboard players add @s points 1\n'
            f'execute if score @s points matches {best_of_number} run function hunt:gameover'
        )

    return(
        f'advancement revoke @a only hunt:dummy_{order_number}\n'
        f'advancement grant @a only hunt:dummy_{order_number + 1}\n'
        'scoreboard players add @s points 1\n'
        f'execute if score @s points matches {best_of_number} run function hunt:gameover'
    )


def write(archive, filepath, destination):
    archive.write(filepath, os.path.join(destination, os.path.basename(filepath)))


def generate_random_zip(fp):
    selected_advancements = random.sample(all_advancements, 5)
    for adv in selected_advancements:
        adv.set_game_mode(adv.MODE_HUNT)
    generate_zip(fp, selected_advancements)


def generate_series_random_zip(fp):
    selected_advancements = random.sample(all_advancements, 25)
    for adv in selected_advancements:
        adv.set_game_mode(adv.MODE_SERIES)

    generate_zip(fp, selected_advancements, 5)


def generate_zip(fp, selected_advancements, best_of_number=None):
    
    with zipfile.ZipFile(fp, 'w') as archive:
        top_folder = 'hunt'
        data_folder = os.path.join(top_folder, 'data')
        hunt_folder = os.path.join(data_folder, 'hunt')
        advancements_folder = os.path.join(hunt_folder, 'advancements')
        functions_folder = os.path.join(hunt_folder, 'functions')
        write(archive, 'pack.mcmeta', top_folder)
        for function in os.listdir('functions'):
            write(archive, os.path.join('functions', function), functions_folder)
        archive.writestr(
            os.path.join(hunt_folder, 'functions', 'advancement.mcfunction'),
            advancement_function(len(selected_advancements))
        )
        write(archive, 'root.json', advancements_folder)
        for number, advancement in enumerate(selected_advancements):
            archive.writestr(
                os.path.join(advancements_folder, advancement.filename),
                advancement.json_dump(number)
            )
            if best_of_number:
                archive.writestr(
                    os.path.join(functions_folder, f'advancement_{number}.mcfunction'),
                    series_advancement_function(order_number=number, best_of_number=best_of_number, total=len(selected_advancements))
                )
                archive.write('dummy.json', os.path.join(advancements_folder, f'dummy_{number}.json'))

# TODO ^ iterate through advancements dict