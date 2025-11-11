import main as m

class text:
    def __init__(self , x , y , text , color):
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.visible = True
        self.text = text
        self.layer = 1
        m.game_instance.layers[1].append(self)
        self.create_text()

    def create_text(self):
        text_surface = m.font_1.render(self.text, True , self.color)
        self.surface = text_surface
        m.game_instance.texts.append(self)
        self.rect = text_surface.get_rect()
        self.rect.center = (self.x , self.y)
        self.pos = self.rect.center

    def update_pos(self):
        self.rect.center = (self.x, self.y)
        self.pos = self.rect.center
    
    def remove(self):
        if self in m.game_instance.texts:
            m.game_instance.texts.remove(self)
        if self in m.game_instance.layers[self.layer]:
            m.game_instance.layers[self.layer].remove(self)
