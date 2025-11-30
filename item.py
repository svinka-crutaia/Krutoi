from soulCoreLib import items

class item():
    def __init__(self, name= 'noNamed item', rary = 0, type = 4, count = 1):
        self.name = name
        raries = ['common', 'rary', 'expensive', 'mistic', 'godness', 'necromantic']
        self.rary = raries[rary]
        types = ['weapon', 'gun', 'ammo', 'spell', 'item', 'quest','food', 'medication']
        self.type = types[type]
        self.count = count
        items.append(self)