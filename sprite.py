import pygame as pg
import soulCoreLib as sc


class sprite:
    def __init__(self , x , y , rotate , img , width = 200, height = 200):
        self.x = x
        self.y = y
        self.rotate = rotate
        self.preImg = img
        self.img = pg.image.load(self.preImg).convert_alpha()
        self.animate_frames = []
        self.animate_frames.append(self.img)
        self.layer = 1
        
        game_instance = sc.game_instance
        game_instance.layers[1].append(self)
        self.clones = []
        self.current_frame = 0
        self.animation_speed = 500  
        self.visible = True
        self.last_animation_time = 0
        self.hasCollider = True
        self.isWall = False
        self.height = height
        self.width = width
        Default_size = (self.height, self.width)
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
        game_instance = sc.game_instance
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
        clone = sc.sprite(x = self.x, y= self.y, rotate= self.rotate, img= self.preImg, width= self.width, height= self.height)
        clone.index = len(self.clones)
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
    
    def remove(self):
        game_instance = sc.game_instance
        if self in game_instance.sprites:
            game_instance.sprites.remove(self)
        if self in game_instance.layers[self.layer]:
            game_instance.layers[self.layer].remove(self)
