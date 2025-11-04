import pygame as pg
import os
import time as t
import keyboard as kb
from pygame import time as pt
from pygame import mixer as pm

pg.init()
pg.font.init()
pm.init()

font_1 = pg.font.SysFont('freesanbold.ttf', 50)
game_instance = None
scene_index = 0
game_locate = os.path.dirname(os.path.abspath(__file__))

class game:
    def __init__(self, height= 800, width= 800, text='unnamed',screen_icon= None, bg_color= (0,0,0)):
        self.height = height
        self.width = width
        self.screen_text = text
        self.screen_icon = screen_icon
        self.run = True
        self.scenes = []
        self.buttons = []
        self.texts = []
        self.player = None
        self.sprites = []
        self.layers = [[] for _ in range(4)]
        self.bg_color = bg_color

        global game_instance
        game_instance = self

    def createWindow(self):
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.screen_text)
        pg.display.set_icon(self.screen_icon)
        
    def eventsCheck(self):
        if self.run:
            for self.e in pg.event.get():
                if self.e.type == pg.QUIT:
                    os.system('cls')
                    print("Приложение отключено!")
                    self.run = False
    def render(self):
        self.screen.fill(self.bg_color)
        
        if self.player:
            self.player.update_person()
        for sprite_obj in self.sprites:
            sprite_obj.update_pos()
        for text_obj in self.texts:
            text_obj.update_pos()
        for button_obj in self.buttons:
            button_obj.update_state()
        
        for layer in self.layers:
            for obj in layer:
                if hasattr(obj, 'root'): 
                    self.screen.blit(obj.root, obj.pos)
                elif hasattr(obj, 'img_rot'): 
                    self.screen.blit(obj.img_rot, obj.pos)
                elif hasattr(obj, 'surface'):
                    self.screen.blit(obj.surface, obj.pos)
                elif hasattr(obj, 'button_img'): 
                    self.screen.blit(obj.button_img, obj.rect)
        
        pg.display.update()
        pg.display.flip()
    

    def isLeft_Mouse(self):
     if self.e:   
        if self.e.type == pg.MOUSEBUTTONDOWN:
            if self.e.button == 1:
                 return True
            
    def isRight_Mouse(self):
     if self.e:   
        if self.e.type == pg.MOUSEBUTTONDOWN:
            if self.e.button == 3:
                 return True
    def isKey_Pressed(self, key):
        if kb.is_pressed(key):
            return True
        else:
            return False
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
        game_instance.scenes.append(self)

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
            game_instance.render()
            game_instance.eventsCheck()
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
        if scene_index + 1 < len(game_instance.scenes):
            scene_index += 1
            game_instance.scenes[scene_index].start_scene(function)
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

class text:
    def __init__(self , x , y , text , color):
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.text = text
        self.layer = 1
        game_instance.layers[1].append(self)
        self.create_text()

    def create_text(self):
        text_surface = font_1.render(self.text, True , self.color)
        self.surface = text_surface
        game_instance.texts.append(self)
        self.rect = text_surface.get_rect()
        self.rect.center = (self.x , self.y)
        self.pos = self.rect.center

    def update_pos(self):
        self.rect.center = (self.x, self.y)
        self.pos = self.rect.center

class sprite:
    def __init__(self , x , y , rotate , img):
        self.x = x
        self.y = y
        self.rotate = rotate
        self.img = pg.image.load(img).convert_alpha()
        self.animate_frames = []
        self.animate_frames.append(self.img)
        self.layer = 1
        game_instance.layers[1].append(self)
        self.clones = []
        self.current_frame = 0
        self.animation_speed = 500  
        self.last_animation_time = 0
        self.hasCollider = True
        self.isWall = False
        Default_size = (200, 200)
        self.size = Default_size
        self.mask = pg.mask.from_surface(self.animate_frames[self.current_frame])
        
        game_instance.sprites.append(self)
        self.img_scale = pg.transform.scale(self.animate_frames[self.current_frame], self.size)
        self.img_rot = pg.transform.rotate(self.img_scale, self.rotate)
        self.mask = pg.mask.from_surface(self.img_rot)
        self.rect = self.img_rot.get_rect()
        self.rect.center = (self.x, self.y)
        self.pos = self.rect.center

    def update_pos(self):
        if not self.isWall:
            self.img_scale = pg.transform.scale(self.animate_frames[self.current_frame], self.size)
            self.img_rot = pg.transform.rotate(self.img_scale, self.rotate)
            self.mask = pg.mask.from_surface(self.img_rot)
            self.pos = (self.x, self.y)

        if self.isWall:
            self.img_scale = pg.transform.scale(self.animate_frames[self.current_frame], self.size)
            self.img_rot = pg.transform.rotate(self.img_scale, self.rotate)
            self.mask = pg.mask.from_surface(self.img_rot)
            self.rect = self.img_rot.get_rect(center=(self.x, self.y))
            self.pos = self.rect.center 

            player = game_instance.player
            if player is None:
                return
            offset = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            if self.mask.overlap(player.mask, offset):
                player.x, player.y = player.prev_x, player.prev_y
                player.rect.center = (player.x, player.y)
                player.pos = player.rect.center

    def add_frame(self, img):
        self.animate_frames.append(img)

    def clear_frame(self, index):
        self.animate_frames.insert(index)
    
    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.last_animation_time = current_time
            
            self.current_frame = (self.current_frame + 1) % len(self.animate_frames)
            self.update_pos()
    def get_frame(self):
        return self.current_frame
    
    def set_frame(self, index):
        self.current_frame = index
        self.img_rot = pg.transform.scale(self.animate_frames[self.current_frame], self.size)

    def create_clone(self, name= f'noName'):
        clone.index = len(self.clones)
        clone = self
        clone.name = str(name) + ' ' + str(clone.index)
        self.clones.append(clone)
        return clone
    
    def get_clone(self, name):
        for clone in self.clones:
            if clone.name == name:
                return [clone, True]
        return False
    
    def isTouch(self, other):  
        if self.hasCollider :
            return self.rect.colliderect(other.rect)     
    
    def animate_min_max(self, min, max):
        current_time = pg.time.get_ticks()
        if current_time - self.last_animation_time > self.animation_speed:
            self.last_animation_time = current_time
            self.current_frame = self.current_frame + 1

        if self.current_frame < min or self.current_frame > max:
            self.current_frame = min

class button():
    def __init__(self, text= '', isWorking= True, x= 0 , y= 0, size= 100):
        self.text = text
        self.isWorking = isWorking
        self.x = x
        self.y = y
        self.state = 2
        self.funct = None
        self.size = (100, 100)
        self.frames = []
        self.layer = 3
        game_instance.layers[3].append(self)
        game_instance.buttons.append(self)
        self.set_button()

        self.default_img = pg.Surface((size, size))
        self.default_img.fill((100, 100, 100))  
        self.frames.append(self.default_img)  
        self.frames.append(self.default_img)  
        self.frames.append(self.default_img)  
        
        game_instance.buttons.append(self)
        self.set_button()

    def set_button(self):
        if 0 <= self.state < len(self.frames):
            self.button_img = pg.transform.scale(self.frames[self.state], self.size)
            self.rect = self.button_img.get_rect()
            self.rect.center = (self.x, self.y)
            self.pos = self.rect.center

    def set_frames(self, onFocus, default, onClick):
        self.frames.clear()
        
        onFocus_img = pg.image.load(onFocus).convert_alpha()
        self.frames.append(onFocus_img)

        default_img = pg.image.load(default).convert_alpha()
        self.frames.append(default_img)

        onClick_img = pg.image.load(onClick).convert_alpha()
        self.frames.append(onClick_img)

        self.set_button()

    def isMouse_focus(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    
    def isButton_pressed(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return game_instance.isLeft_Mouse()
    
    def update_state(self):
        if self.isMouse_focus() and not game_instance.isLeft_Mouse():
            self.state = 0
            self.img = self.frames[0]

        if self.isButton_pressed():
            self.state = 1
            self.funct()
        
        if not self.isMouse_focus():
            self.state = 2

        self.button_img = pg.transform.scale(self.frames[self.state], self.size)
        self.pos = (self.x , self.y)

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
        self.layer = 2
        game_instance.layers[2].append(self)
        self.mag_damage = 0
        self.mag_armor = 1
        self.name = name
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
