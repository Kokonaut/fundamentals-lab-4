import pyglet

from engine.util import get_files_in_path


class MonsterSprite:

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    IDLE = 'idle'

    def __init__(self, id, path, x, y, speed, health, batch=None, group=None, action=IDLE):
        self.id = id
        self.path = path
        self.batch = batch
        self.group = group
        # These are the true x/y we consider the sprite to be at
        self.x = x
        self.y = y
        self.scale = 0.25
        self.animation = None
        # Sprite x/y is offset due to the anchor point not being in center
        self.sprite = self._generate_sprite()
        self.action = action
        self.speed = speed
        self.health = health
        self.current_health = health
        self.dest_x = None
        self.dest_y = None

        self.max_health_width = 40
        self.health_bar = self.get_health_bar()

        self.is_defeated = False

    def _generate_sprite(self):
        walk_path = self.path + "move/"
        defeated_path = self.path + "defeated/"
        # Set up animation for character sprite
        walk_frames = [pyglet.resource.image(walk_path + f)
                       for f in get_files_in_path(walk_path)]
        defeated_frames = [pyglet.resource.image(defeated_path + f)
                           for f in get_files_in_path(defeated_path)]
        self.walk_animation = pyglet.image.Animation.from_image_sequence(
            walk_frames,
            duration=0.1,
            loop=True
        )
        self.defeated_animation = pyglet.image.Animation.from_image_sequence(
            defeated_frames,
            duration=0.05,
            loop=False
        )

        self.animation = self.walk_animation

        # Set up character sprite
        monster_sprite = pyglet.sprite.Sprite(
            self.animation,
            group=self.group,
            batch=self.batch,
            x=self.convert_x(),
            y=self.convert_y()
        )
        monster_sprite.scale = self.scale

        return monster_sprite

    def convert_x(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.x - self.animation.get_max_width() * self.scale / 2

    def convert_y(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.y - self.animation.get_max_height() * self.scale / 6
        # return self.y

    def at_destination(self):
        return self.dest_x == None and self.dest_y == None

    def update(self, dt):
        # If destination not set, then don't move
        if self.is_defeated:
            if self.sprite.image != self.defeated_animation:
                self.sprite.image = self.defeated_animation
            return True
        else:
            self.health_bar.x = self.x - int(self.sprite.width * 3/8)
            self.health_bar.y = self.y + self.sprite.height
            new_width = self.max_health_width * \
                (self.current_health / self.health)
            if new_width >= 0:
                self.health_bar.width = new_width
            if self.current_health <= 0:
                self.is_defeated = True

        if self.at_destination():
            return True

        if self.action == MonsterSprite.UP:
            reached_dest = self.move_up(self.speed, dt, self.dest_y)
        elif self.action == MonsterSprite.DOWN:
            reached_dest = self.move_down(self.speed, dt, self.dest_y)
        elif self.action == MonsterSprite.RIGHT:
            reached_dest = self.move_right(self.speed, dt, self.dest_x)
        elif self.action == MonsterSprite.LEFT:
            reached_dest = self.move_left(self.speed, dt, self.dest_x)
        elif self.action == MonsterSprite.IDLE:
            reached_dest = True
        else:
            raise ValueError(
                "Got an unsupported action: {d}".format(d=self.action)
            )
        if reached_dest:
            self.wipe_destination()
        return reached_dest

    def wipe_destination(self):
        self.dest_x = None
        self.dest_y = None

    def move_up(self, speed, dt, dest_y):
        new_y = self.y + speed * dt
        reached_destination = False
        if new_y > dest_y:
            self.y = dest_y
            reached_destination = True
        else:
            self.y = new_y
        self.sprite.y = self.convert_y()
        return reached_destination

    def move_down(self, speed, dt, dest_y):
        new_y = self.y - speed * dt
        reached_destination = False
        if new_y < dest_y:
            self.y = dest_y
            reached_destination = True
        else:
            self.y = new_y
        self.sprite.y = self.convert_y()
        return reached_destination

    def move_right(self, speed, dt, dest_x):
        new_x = self.x + speed * dt
        reached_destination = False
        if new_x > dest_x:
            self.x = dest_x
            reached_destination = True
        else:
            self.x = new_x
        self.sprite.x = self.convert_x()
        return reached_destination

    def move_left(self, speed, dt, dest_x):
        new_x = self.x - speed * dt
        reached_destination = False
        if new_x < dest_x:
            self.x = dest_x
            reached_destination = True
        else:
            self.x = new_x
        self.sprite.x = self.convert_x()
        return reached_destination

    def damage(self, damage_amount):
        print("{monster_id} got damaged for {dmg}".format(
            monster_id=self.id, dmg=damage_amount))
        self.current_health = max(0, self.current_health - damage_amount)

    def get_health_bar(self):
        health_bar = pyglet.shapes.Rectangle(
            self.x, self.y + self.sprite.height,
            self.max_health_width,
            5,
            color=(255, 0, 0),
            batch=self.batch,
            group=self.group
        )
        return health_bar

    def hide(self):
        self.sprite.visible = False
        self.health_bar.visible = False
