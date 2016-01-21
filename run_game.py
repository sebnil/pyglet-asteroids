# force python 3.* compability
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
# regular imports below:
import pyglet
from pyglet import clock, font, image, window
from pyglet.gl import *
from random import uniform
from game import entities, resources
from pyglet.window import key
from game.util import distance

window_dimensions = (800, 600)

class World(object):

    def __init__(self):
        self.game_objects = []
        self.player = entities.Player()
        self.game_objects.append(self.player)
        clock.schedule_interval(self.spawn_asteroid, 1)
        clock.schedule_interval(self.update, 1/120)

    def spawn_asteroid(self, dt):
        #[obj for obj in self.game_objects if isinstance(obj, entities.Asteroid)]
        if len([obj for obj in self.game_objects if isinstance(obj, entities.Asteroid)]) < 20:
            size = uniform(0.8, 1.0)
            x, y = self.player.x, self.player.y
            while distance((x, y), (self.player.x, self.player.y)) < 100:
                x = uniform(-window_dimensions[0]/2, window_dimensions[0]/2)
                y = uniform(-window_dimensions[1]/2, window_dimensions[1]/2)
            rot = uniform(0.0, 360.0)
            velocity_x = uniform(-30, 30)
            velocity_y = uniform(5, 3)
            ent = entities.Asteroid(size, x, y, rot, velocity_x, velocity_y)
            self.game_objects.append(ent)
            return ent

    def update(self, dt):

        for obj_1 in self.game_objects:
            for obj_2 in self.game_objects:
                if obj_1 is obj_2:
                    continue
                if not obj_1.dead and not obj_2.dead:
                    if obj_1.collides_with(obj_2):
                        obj_1.handle_collision_with(obj_2)
                        obj_2.handle_collision_with(obj_1)

        for obj in self.game_objects:
            obj.update(dt)
            self.game_objects.extend(obj.new_objects)
            obj.new_objects = []

        ids_to_remove = [obj for obj in self.game_objects if obj.dead]
        for id_to_remove in ids_to_remove:
            self.game_objects.remove(id_to_remove)

        #del self.game_objects[ga]

    def draw(self):


        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        resources.background_image.blit(-400,-300, width=800, height=600)
        for ent in self.game_objects:
            ent.draw()


class Camera(object):

    def __init__(self, win, x=0.0, y=0.0, rot=0.0, zoom=1.0):
        self.win = win
        self.x = x
        self.y = y
        self.rot = rot
        self.zoom = zoom

    def worldProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        widthRatio = self.win.width / self.win.height
        gluOrtho2D(
            -self.zoom * widthRatio,
            self.zoom * widthRatio,
            -self.zoom,
            self.zoom)

    def hudProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.win.width, 0, self.win.height)


class Hud(object):

    def __init__(self, win):
        self.fps = clock.ClockDisplay()

    def draw(self):
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        self.fps.draw()

class App(object):

    def __init__(self):
        self.world = World()
        self.win = window.Window(fullscreen=False, vsync=True, width=window_dimensions[0], height=window_dimensions[1])
        self.camera = Camera(self.win, zoom=200.0)
        self.hud = Hud(self.win)


        self.win.push_handlers(self.world.player.key_handler)

        clock.set_fps_limit(60)

    def mainLoop(self):
        while not self.win.has_exit:
            self.win.dispatch_events()

            #self.world.tick()

            self.camera.worldProjection()
            self.world.draw()

            self.camera.hudProjection()
            self.hud.draw()

            clock.tick()
            self.win.flip()

            if self.world.player.dead is True:
                self.world = World()
                self.win.push_handlers(self.world.player.key_handler)

app = App()
app.mainLoop()
