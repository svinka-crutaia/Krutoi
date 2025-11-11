import pygame as pg
from pygame import time as pt
import main as m
from pygame import mixer as pm

class scene:


    def __init__(self, name, fps= 20):
        self.isRun = False
        self.state = 'Stopped'
        self.name = name
        self.obj = []
        self.cycles_loop = []
        self.cycles_setup = []
        self.fps = fps
        self.clock = pt.Clock()
        self.music = None
        self.delay_start = 0
        self.delay_duration = 0
        self.delay_active = False
        m.game_instance.scenes.append(self)

    def set_bg_music(self, music, volume= 1):
        if music:
            self.music = pm.music.load(music)
            pm.music.set_volume(volume)
            pm.music.play()

    def start_scene(self, function):
        self.isRun = True
        self.state = 'Working'
        if self.isRun:
            for func in self.cycles_setup:
                func()

        while self.isRun:

            self.clock.tick(int(self.fps))
            m.game_instance.render()
            m.game_instance.eventsCheck()
            self.cycles_loop.append(function)

            for func in self.cycles_loop:
                func()

            if self.isRun == False:
                break
    def add_loop_cycle(self, function):
        self.cycles_loop.append(function)

    def off_loop_cycle(self, index):
        self.cycles_loop.insert(self, index)
    
    def add_setup_cycle(self, function):
        self.cycles_setup.append(function)

    def off_setup_cycle(self, index):
        self.cycles_setup.insert(self, index)

    def off_scene(self):
        self.isRun = False
        self.state = 'Stopped'

    def next_scene(self, function):
        global scene_index  
        self.off_scene() 
        if scene_index + 1 < len(m.game_instance.scenes):
            scene_index += 1
            m.game_instance.scenes[scene_index].start_scene(function)
        else:
            print("Error: Unexpected Scenes Massive In Game Obj")
            
    def start_delay(self, delay_ms):
        self.delay_start = pg.time.get_ticks()
        self.delay_duration = delay_ms
        self.delay_active = True
    
    def is_delay_finished(self):
        if self.delay_active and pg.time.get_ticks() - self.delay_start >= self.delay_duration:
            self.delay_active = False
            return True
        return False