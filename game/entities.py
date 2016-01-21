# force python 3.* compability
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
# regular imports below:
from pyglet.gl import *
from game import resources, util
from pyglet.window import key
import math
import random

class Asteroid_Vertex(object):

    def __init__(self, id, size, x, y, rot, velocity_x, velocity_y):
        self.id = id
        self.size = size
        self.x = x
        self.y = y
        self.rot = rot
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self, dt):
        self.rot += 10.0 / self.size
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def draw(self):
        glLoadIdentity()
        glTranslatef(self.x, self.y, 0.0)
        glRotatef(self.rot, 0, 0, 1)
        glScalef(self.size, self.size, 1.0)
        glBegin(GL_TRIANGLES)
        #glColor4f(1.0, 0.0, 0.0, 0.0)
        glVertex2f(0.0, 0.5)
        #glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex2f(0.2, -0.5)
        #glColor4f(0.0, 0.0, 1.0, 1.0)
        glVertex2f(-0.2, -0.5)
        glEnd()


class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.dead = False
        self.new_objects = []

    def collides_with(self, other_object):
        collision_distance = self.image.width/2*self.scale + other_object.image.width/2*self.scale
        actual_distance = util.distance( self.position, other_object.position)
        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        if other_object.__class__ == self.__class__:
            self.dead = False
        else:
            self.dead = True

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        self.check_bounds()

    def check_bounds(self):
        min_x = -280
        min_y = -220
        max_x = 280
        max_y = 220
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

class Asteroid(PhysicalObject):
    def __init__(self, size, x, y, rot, velocity_x, velocity_y):
        super(Asteroid, self).__init__(img=resources.asteroid_images[random.randint(0,8)])
        self.size = size
        self.x = x
        self.y = y
        self.rot = rot
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.scale = self.size

    def update(self, dt):
        super(Asteroid, self).update(dt)
        self.rotation += 1.0 / self.size

    def handle_collision_with(self, other_object):
        super(Asteroid, self).handle_collision_with(other_object)
        if self.dead and self.size > 0.25:
            num_asteroids = random.randint(2, 3)
            for i in range(num_asteroids):
                new_asteroid = Asteroid(
                    x=self.x, y=self.y,
                    rot = random.randint(0, 360),
                    velocity_x = random.random() * 30 + self.velocity_x,
                    velocity_y = random.random() * 30 + self.velocity_y,
                    size = self.scale * 0.5,
                )
                self.new_objects.append(new_asteroid)

    def draw(self):
        glLoadIdentity()
        #glRotatef(self.rot, 0, 0, 1)
        #glScalef(self.size/100, self.size/100, 1.0)
        super(Asteroid, self).draw()

class Player(PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)

        self.engine_sprite = pyglet.sprite.Sprite( img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = True

        self.key_handler = key.KeyStateHandler()

        self.scale = 0.5

        #self.player_sprite = pyglet.sprite.Sprite( img=resources.player_image, x=40, y=30)
        #super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        self.x = 40
        self.y = -50
        self.velocity_x = 0
        self.velocity_y = 0

        self.thrust = 300
        self.rotate_speed = 200

        self.bullet_speed = 200.0

        self.bullet_loaded = True

    def update(self, dt):
        super(Player, self).update(dt)

        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        elif self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        if self.key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = -math.sin(angle_radians) * self.thrust * dt
            force_y = math.cos(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y

            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True
        else:
            self.engine_sprite.visible = False

        if self.key_handler[key.SPACE] and self.bullet_loaded:
            self.fire()
            self.bullet_loaded = False
            pyglet.clock.schedule_once(self.reload_bullet, 0.1)

    def handle_collision_with(self, other_object):
        if isinstance(other_object, Asteroid):
            self.dead = True

    def fire(self):
        angle_radians = -math.radians(self.rotation-90)
        ship_radius = self.image.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = Bullet(bullet_x, bullet_y, batch=self.batch)

        bullet_vx = (
            self.velocity_x +
            math.cos(angle_radians) * self.bullet_speed
        )
        bullet_vy = (
            self.velocity_y +
            math.sin(angle_radians) * self.bullet_speed
        )
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy

        self.velocity_x -= bullet_vx*0.05
        self.velocity_y -= bullet_vy*0.05

        self.new_objects.append(new_bullet)

    def reload_bullet(self, dt):
        self.bullet_loaded = True


    def draw(self):
        #glLoadIdentity()
        super(Player, self).draw()
        self.engine_sprite.draw()



class Bullet(PhysicalObject):
    """Bullets fired by the player"""

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(
            resources.bullet_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 1)

    def die(self, dt):
        self.dead = True