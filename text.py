import soulCoreLib as sc
from soulCoreLib import font_1


class text:
    def __init__(self , x , y , text , color):
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.visible = True
        self.text = text
        self.layer = 1
        game_instance = sc.game_instance

        if game_instance is None:
            raise RuntimeError("game_instance not initialized. Create gameClass instance first.")
        game_instance.layers[1].append(self)
        self.create_text()

    def create_text(self):
        game_instance = sc.game_instance
        text_surface = font_1.render(self.text, True , self.color)
        self.surface = text_surface
        game_instance.texts.append(self)
        self.rect = text_surface.get_rect()
        self.rect.center = (self.x , self.y)
        self.pos = self.rect.center

    def update_pos(self):
        self.rect.center = (self.x, self.y)
        self.pos = self.rect.center
    
    def remove(self):
        game_instance = sc.game_instance
        if self in game_instance.texts:
            game_instance.texts.remove(self)
        if self in game_instance.layers[self.layer]:
            game_instance.layers[self.layer].remove(self)
