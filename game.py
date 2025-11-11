import pygame as pg
import os
import keyboard as kb
import main as m

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
        m.game_instance = self

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
        
        if self.player and self.player.visible :
            self.player.update_person()
        for sprite_obj in self.sprites:
            if sprite_obj.visible:
                sprite_obj.update_pos()
        for text_obj in self.texts:
            if text_obj.visible:
                text_obj.update_pos()
        for button_obj in self.buttons:
            if button_obj.visible:
                button_obj.update_state()
        
        for layer in self.layers:
            for obj in layer:
                if hasattr(obj, 'visible') and not obj.visible:
                    continue
                if hasattr(obj, 'root') : 
                    self.screen.blit(obj.root, obj.pos)
                elif hasattr(obj, 'img_rot') : 
                    self.screen.blit(obj.img_rot, obj.pos)
                elif hasattr(obj, 'surface') :
                    self.screen.blit(obj.surface, obj.pos)
                elif hasattr(obj, 'button_img') : 
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