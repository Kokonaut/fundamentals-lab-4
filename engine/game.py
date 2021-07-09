import pyglet
import random
import time

from engine.monster import MonsterSprite
from engine.grid import Grid
from engine.log_spam import LogSpam
from engine.spawner import Spawner
from engine.throwable import Throwable
from engine.tower import TowerSprite


class Game:

    CHARACTER_SPEED = 100  # Character movement in pixels per second
    FPS = 30  # frames per second (aka speed of the game)
    THROW_DISTANCE = 2

    def __init__(self, window, rows, cols, lives=3):
        pyglet.font.add_file('assets/PressStart2P-Regular.ttf')
        self.font = pyglet.font.load('Press Start 2P')

        # Set up batch and ordered groups
        self.bg_batch = pyglet.graphics.Batch()
        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.terrainground = pyglet.graphics.OrderedGroup(2)
        self.monster_layer = pyglet.graphics.OrderedGroup(3)
        self.finish_ground = pyglet.graphics.OrderedGroup(4)
        self.foreground = pyglet.graphics.OrderedGroup(5)

        # Set up window and grid variables
        self.window = window
        self.window_block_width = cols
        self.cols = cols
        self.rows = rows
        self.grid = Grid(self.rows, self.cols, self.window.width)

        # Set up background
        bg_image = pyglet.image.load('assets/background/main_bg.png')
        self.bg_sprite = pyglet.sprite.Sprite(
            bg_image,
            batch=self.bg_batch,
            group=self.background
        )
        height_scale = self.window.height / self.bg_sprite.height
        width_scale = self.window.width / self.bg_sprite.width
        self.bg_sprite.scale = max(height_scale, width_scale)

        self.lives = lives
        self.draw_life_counter()

        # Set up character sprite info
        self.characters = dict()
        self.throwables = list()

        # State keeping variables
        self.lock = False
        self.game_over_timer = 3
        self.safety_counter = 10
        self.log_spam = LogSpam()

        # Set up environment objects
        self.obstacles = dict()
        self.terrain = dict()
        self.tower_spots = dict()
        self.towers = dict()
        self.spawners = list()

        self.finish = None
        self.num_goals = 0

        # Lab decision generator
        self.decision_func = None

    def on_draw(self):
        self.window.clear()
        self.bg_batch.draw()
        self.main_batch.draw()

    def start_game(self):
        self.window.push_handlers(
            on_draw=self.on_draw,
        )
        pyglet.clock.schedule_interval(self.update, 1.0 / self.FPS)

    def stop_game(self):
        print('Game shutting down')
        time.sleep(5)
        pyglet.clock.unschedule(self.update)
        self.window.remove_handlers()
        pyglet.app.exit()

    def add_decision_func(self, func):
        self.decision_func = func

    def set_character_commands(self, commands):
        self.commands = commands

    def update(self, dt):
        # Game is over and controls locked
        if self.lock:
            self.game_over_timer -= dt
            if self.game_over_timer <= 0:
                self.stop_game()

        game_over = True
        monsters = list()
        for spawner in self.spawners:
            spawner.update(dt)
            if len(spawner.monster_queue) > 0:
                game_over = False
            for monster in spawner.spawned:
                if monster.at_destination():
                    spawner.spawned.remove(monster)
                    monster.hide()
                    self.lives = max(self.lives - 1, 0)
                    self.update_life_label(self.lives)
                elif not monster.is_defeated:
                    monsters.append(monster)

        if len(monsters) > 0:
            game_over = False

        if self.lives <= 0:
            if not self.lock:
                print("Game Over, you lost all your lives")
            self.lock = True

        if game_over:
            if self.safety_counter > 0:
                self.safety_counter -= 1
                return
            if not self.lock:
                print("You Win! With {lives} lives remaining!".format(
                    lives=self.lives))
            self.lock = True

        for key in self.towers:
            # Just to throw a wrench into the lab
            random.shuffle(monsters)
            tower = self.towers[key]
            tower.update(dt, monsters)

    def _add_terrain(self, path, x, y, group):
        obstacle_image = pyglet.resource.image(path)
        obstacle_image.anchor_x = obstacle_image.width // 2
        obstacle_image.anchor_y = obstacle_image.height // 2
        obstacle_sprite = pyglet.sprite.Sprite(
            obstacle_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=group
        )
        height_scale = self.grid.cell_length / obstacle_sprite.height
        width_scale = self.grid.cell_length / obstacle_sprite.width
        obstacle_sprite.scale = min(height_scale, width_scale)
        return obstacle_sprite

    def add_terrain(self, path, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_terrain(path, x, y, self.terrainground)
            self.terrain[coord_name] = sprite

    def add_finish(self, coord):
        x, y = self.grid.calculate_xy_from_name(coord)
        finish_image = pyglet.resource.image('assets/finish.png')
        finish_image.anchor_x = finish_image.width // 2
        finish_image.anchor_y = finish_image.height // 2
        self.finish = pyglet.sprite.Sprite(
            finish_image,
            batch=self.main_batch,
            x=x,
            y=y + self.grid.cell_length // 4,  # Account for offset of road
            group=self.finish_ground
        )
        self.finish.scale = 0.33

    def add_tower_spots(self, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_spot(x, y)
            self.tower_spots[coord_name] = sprite

    def _add_spot(self, x, y):
        spot_image = pyglet.resource.image('assets/background/dot.png')
        spot_image.anchor_x = spot_image.width // 2
        spot_image.anchor_y = spot_image.height
        spot_sprite = pyglet.sprite.Sprite(
            spot_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.terrainground
        )
        spot_sprite.scale = 0.5
        return spot_sprite

    def add_tower(self, coord):
        x, y = self.grid.calculate_xy_from_name(coord)
        tower_sprite = TowerSprite(x, y, self.main_batch)
        self.towers[coord] = tower_sprite

    def add_spawner(self, coord, dest_coord, config):
        self.spawners.append(
            Spawner(config, coord, dest_coord, self.grid,
                    self.main_batch, self.monster_layer)
        )

    def add_selector_func(self, key, func):
        tower = self.towers[key]
        tower.set_selector_func(func)

    def draw_life_label(self):
        self.life_label = pyglet.text.Label(
            text="",
            x=self.window.width * 0.80,
            y=self.window.height * 0.90,
            font_name='Press Start 2P',
            font_size=18,
            anchor_x='left',
            batch=self.main_batch,
            group=self.foreground
        )
        self.life_label.draw()

    def draw_life_counter(self):
        self.draw_life_label()
        self.update_life_label(self.lives)
        life_icon = pyglet.resource.image(
            'assets/heart.png'
        )
        life_icon.anchor_x = life_icon.width * 1.5
        life_icon.anchor_y = life_icon.height * 0.1
        self.life_sprite = pyglet.sprite.Sprite(
            life_icon,
            x=self.window.width * 0.8,
            y=self.window.height * 0.9,
            batch=self.main_batch,
            group=self.foreground
        )

    def update_life_label(self, lives):
        self.life_label.text = "Lives: {lives}".format(lives=lives)
