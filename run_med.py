import pyglet
from engine.game import Game
from lab import lab_run_med

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

monster_config = [
    {
        'type': 'heavy',
        'cooldown': 0,
    },
    {
        'type': 'heavy',
        'cooldown': 2,
    },
    {
        'type': 'fast',
        'cooldown': 4,
    },
    {
        'type': 'fast',
        'cooldown': 5,
    },
    {
        'type': 'fast',
        'cooldown': 2,
    },
    {
        'type': 'fast',
        'cooldown': 3,
    },
    {
        'type': 'fast',
        'cooldown': 2,
    },
]

game.add_spawner(
    'a4', 'p4', monster_config
)

game.add_tower_spots(['i6', 'c6'])
game.add_tower('i6')
game.add_selector_func(
    'i6', lab_run_med
)

game.add_tower('c6')
game.add_selector_func('c6', lab_run_med)


if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
