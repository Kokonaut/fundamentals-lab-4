import pyglet
import random

from engine.game import Game
from lab import lab_run_big_1, lab_run_big_2, lab_run_big_3, lab_run_big_4

window_width = 1400
rows = 9
cols = 16
window_ratio = cols / rows
window_height = int(window_width / window_ratio)

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

alph = 'abcdefghijklmnopq'
road_coords = list()
for i in range(cols):
    road_coords.append(alph[i] + '4')
game.add_terrain('assets/background/road.png', road_coords)

game.add_finish('p4')

monster_config = list()

for _ in range(100):
    type_dice = random.randint(0, 4)
    monster_type = None
    if type_dice == 0:
        monster_type = 'heavy'
    else:
        monster_type = 'fast'

    cooldown = random.uniform(0.2, 5.0)
    monster_config.append(
        {
            'type': monster_type,
            'cooldown': cooldown
        }
    )


game.add_spawner(
    'a4', 'p4', monster_config
)

game.add_tower_spots(['i6', 'c6', 'g2', 'm2'])
game.add_tower('i6')
game.add_selector_func(
    'i6', lab_run_big_3
)

game.add_tower('c6')
game.add_selector_func('c6', lab_run_big_1)

game.add_tower('g2')
game.add_selector_func('g2', lab_run_big_2)

game.add_tower('m2')
game.add_selector_func('m2', lab_run_big_4)


if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
