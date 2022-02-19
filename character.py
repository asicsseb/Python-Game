class Character:
    def __init__(self, a, b, c, d, e):
        self.name = a
        self.health = b
        self.int = c
        self.cha = d
        self.fort = e
    
    def updateAtr(atribute, change):
        atribute += change
