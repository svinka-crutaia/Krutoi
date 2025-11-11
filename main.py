import pygame as pg
from pygame import mixer as pm

pg.init()
pg.font.init()
pm.init()

font_1 = pg.font.SysFont('freesanbold.ttf', 50)
game_instance = None
scene_index = 0
items = []