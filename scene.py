import pygame as pg
from pygame import time as pt
import soulCoreLib as sc
from pygame import mixer as pm

class scene:
    def __init__(self, name, fps=20):
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

        game_instance = sc.game_instance
        if game_instance is not None:
            game_instance.scenes.append(self)

    def set_bg_music(self, music, volume=1):
        if music:
            pm.music.load(music)
            pm.music.set_volume(volume)
            pm.music.play()

    def start_scene(self, function):
        game_instance = sc.game_instance
        if game_instance is None:
            print(f"Error: game_instance not initialized for scene '{self.name}'")
            return
            
        self.isRun = True
        self.state = 'Working'
    
        for func in self.cycles_setup:
            func()

        self.cycles_loop.append(function)

        while self.isRun:
            self.clock.tick(int(self.fps))
            game_instance.eventsCheck()
            game_instance.render()
        
            for func in self.cycles_loop:
                func()

            if not self.isRun:
                break

    def add_loop_cycle(self, function):
        self.cycles_loop.append(function)

    def off_loop_cycle(self, index):
        if 0 <= index < len(self.cycles_loop):
            self.cycles_loop.pop(index)
    
    def add_setup_cycle(self, function):
        self.cycles_setup.append(function)

    def off_setup_cycle(self, index):
        if 0 <= index < len(self.cycles_setup):
            self.cycles_setup.pop(index)

    def off_scene(self):
        self.isRun = False
        self.state = 'Stopped'

    def next_scene(self, function):
        game_instance = sc.game_instance
        if game_instance is None:
            print("Error: game_instance not initialized")
            return
            
        self.off_scene()
        
        if self in game_instance.scenes:
            current_index = game_instance.scenes.index(self)
            
            if current_index + 1 < len(game_instance.scenes):
                next_scene = game_instance.scenes[current_index + 1]
                print(f"Switching from scene '{self.name}' to scene '{next_scene.name}'")
                next_scene.start_scene(function)
            else:
                print("No more scenes available. This was the last scene.")
        else:
            print("Error: Current scene not found in game_instance.scenes")

    def start_delay(self, delay_ms):
        self.delay_start = pg.time.get_ticks()
        self.delay_duration = delay_ms
        self.delay_active = True
    
    def is_delay_finished(self):
        if self.delay_active and pg.time.get_ticks() - self.delay_start >= self.delay_duration:
            self.delay_active = False
            return True
        return False