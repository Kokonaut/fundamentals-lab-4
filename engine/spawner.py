from engine.monster import MonsterSprite


FAST_SPEED = 80
FAST_HEALTH = 25

HEAVY_SPEED = 35
HEAVY_HEALTH = 120


class Spawner:

    def __init__(self, config, position_name, dest_name, grid, batch, group=None):
        self.config = config
        self.monster_queue = list()
        self.spawned = list()
        self.interval = self.config[0]['cooldown']
        self.xy = grid.calculate_xy_from_name(position_name)
        self.xy = (self.xy[0] - grid.cell_length, self.xy[1],)
        self.dest_xy = grid.calculate_xy_from_name(dest_name)
        self.batch = batch
        self.group = group

        self.monster_index = 0

        self.load_in_monsters()

    def load_in_monsters(self):
        for i in range(len(self.config)):
            spawn = self.config[i]
            monster_id = "monster_" + str(i)
            if spawn['type'] == 'fast':
                self.monster_queue.append(self.load_fast_monster(monster_id))
            elif spawn['type'] == 'heavy':
                self.monster_queue.append(self.load_heavy_monster(monster_id))
            else:
                raise ValueError(
                    'Unsupported Monster Type: ' + spawn['type'])

    def update(self, dt):
        self.run_spawn(dt)
        for sprite in self.spawned:
            sprite.update(dt)

    def run_spawn(self, dt):
        if len(self.monster_queue) == 0:
            return
        if self.interval <= 0:
            sprite = self.monster_queue.pop(0)
            self.spawned.append(sprite)
            print("Spawning monster: {id}".format(id=sprite.id))
            sprite.action = MonsterSprite.RIGHT
            sprite.sprite.visible = True
            self.monster_index += 1
            self.interval = self.get_interval_to_next_spawn()
        else:
            self.interval -= dt

    def get_interval_to_next_spawn(self):
        if len(self.monster_queue) == 0:
            return 999
        next_spawn = self.config[self.monster_index]
        return next_spawn['cooldown']

    def load_fast_monster(self, monster_id):
        sprite = MonsterSprite(
            monster_id,
            'assets/enemy_2/',
            self.xy[0],
            self.xy[1],
            FAST_SPEED,
            FAST_HEALTH,
            batch=self.batch,
            group=self.group,
            action=MonsterSprite.IDLE
        )
        sprite.sprite.visible = False
        sprite.dest_x = self.dest_xy[0]
        sprite.dest_y = self.dest_xy[1]
        return sprite

    def load_heavy_monster(self, monster_id):
        sprite = MonsterSprite(
            monster_id,
            'assets/enemy_1/',
            self.xy[0],
            self.xy[1],
            HEAVY_SPEED,
            HEAVY_HEALTH,
            batch=self.batch,
            group=self.group,
            action=MonsterSprite.RIGHT
        )
        sprite.sprite.visible = False
        sprite.dest_x = self.dest_xy[0]
        sprite.dest_y = self.dest_xy[1]
        return sprite
