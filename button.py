import pygame as pg
import main as m


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
        m.game_instance.layers[3].append(self)
        m.game_instance.buttons.append(self)
        self.set_button()
        self.visible = True
        self.width = size
        self.height = size

        self.default_img = pg.Surface((self.width, self.height))
        self.default_img.fill((100, 100, 100))  
        self.frames.append(self.default_img)  
        self.frames.append(self.default_img)  
        self.frames.append(self.default_img)  
        
        m.game_instance.buttons.append(self)
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
            return m.game_instance.isLeft_Mouse()
    
    def update_state(self):
        if self.isMouse_focus() and not m.game_instance.isLeft_Mouse():
            self.state = 0
            self.img = self.frames[0]

        if self.isButton_pressed():
            self.state = 1
            self.funct()
        
        if not self.isMouse_focus():
            self.state = 2

        self.button_img = pg.transform.scale(self.frames[self.state], self.size)
        self.pos = (self.x , self.y)
    
    def remove(self):
        if self in m.game_instance.texts:
            m.game_instance.buttons.remove(self)
        if self in m.game_instance.layers[self.layer]:
            m.game_instance.layers[self.layer].remove(self)