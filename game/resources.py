# force python 3.* compability
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
# regular imports below:

import pyglet
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

background_image = pyglet.resource.image('background.png')

player_image = pyglet.resource.image('ship.png')

engine_image = pyglet.resource.image("fire.png")
engine_image.anchor_x = engine_image.width / 2
engine_image.anchor_y = engine_image.height+9

bullet_image = pyglet.resource.image('shooting3.png')
asteroid_images = [
    pyglet.resource.image('object_1.png'),
    pyglet.resource.image('object_2.png'),
    pyglet.resource.image('object_3.png'),
    pyglet.resource.image('object_4.png'),
    pyglet.resource.image('object_5.png'),
    pyglet.resource.image('object_6.png'),
    pyglet.resource.image('object_7.png'),
    pyglet.resource.image('object_8.png'),
    pyglet.resource.image('object_9.png'),
    ]

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

center_image(player_image)
center_image(bullet_image)
for asteroid_image in asteroid_images:
    center_image(asteroid_image)