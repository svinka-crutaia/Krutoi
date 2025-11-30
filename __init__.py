from .game import gameClass
import pygame as pg

game_instance = None
font_1 = pg.font.SysFont('freesanbold.ttf', 50)
scene_index = 0
items = []

from .button import button
from .item import item
from .player import player
from .scene import scene
from .sprite import sprite
from .text import text



__version__ = "0.1.0"