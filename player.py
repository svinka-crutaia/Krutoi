import pygame as pg
import soulCoreLib as sc

class player():
    def __init__(self, name= 'noName', down_idle= '', down_0= '', down_1= '' , up_idle= ''):
        self.healh = 500
        self.xp = 0
        self.lvl = 0
        self.debuffs = []
        self.buffs = []
        self.state = 'down'
        self.x = 300
        self.y = 300
        self.speed = 10
        self.damage = 10
        self.armor = 0
        self.visible = True
        self.layer = 2
        game_instance = sc.game_instance
        game_instance.layers[2].append(self)
        self.mag_damage = 0
        self.mag_armor = 1
        self.name = name
        self.inv = []
        self.frames = []  
        down_idle_img = pg.image.load(down_idle)
        self.frames.append(down_idle_img)
        down_0_img = pg.image.load(down_0)
        self.frames.append(down_0_img)
        down_1_img = pg.image.load(down_1)
        self.frames.append(down_1_img)
        up_idle_img = pg.image.load(up_idle)
        self.frames.append(up_idle_img)
        self.size = (200, 200)
        game_instance.player = self
        self.current_frame = 0
        self.last_animation_time = 0
        self.animation_speed = 200
        self.root = pg.transform.scale(self.frames[self.current_frame], self.size)
        self.rect = self.root.get_rect()
        self.mask = pg.mask.from_surface(self.root)
        self.rect.center = (self.x, self.y)
        self.pos = self.rect.center

    def animate_min_max(self, min, max):
        current_time = pg.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame = self.current_frame + 1

        if self.current_frame < min or self.current_frame > max:
            self.current_frame = min

    def update_person(self):
        game_instance = sc.game_instance
        self.prev_x = self.x
        self.prev_y = self.y
        
        self.pos = (self.x, self.y)
        self.root = pg.transform.scale(self.frames[self.current_frame], self.size)
        self.mask = pg.mask.from_surface(self.root)
        self.rect = self.root.get_rect()
        self.rect.center = self.pos
        
        if game_instance.isKey_Pressed('s'): 
            self.y += self.speed
            self.animate_min_max(1,2)
            self.state = 'down'
        elif game_instance.isKey_Pressed('w'): 
            self.y -= self.speed
            self.state = 'up'
        elif game_instance.isKey_Pressed('d'): 
            self.x += self.speed
            self.state = 'right'
        elif game_instance.isKey_Pressed('a'):  
            self.x -= self.speed
            self.state = 'left'
        
        self.pos = (self.x, self.y)
        self.rect.center = self.pos
        
        if not game_instance.isKey_Pressed('s') and self.state == 'down':
            self.current_frame = 0
        if not game_instance.isKey_Pressed('w') and self.state == 'up':
            self.current_frame = 3

    def isPlayer_touch(self, other):
        return self.rect.colliderect(other)
    