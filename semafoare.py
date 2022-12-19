import pygame

class Semafor:
    def __init__(self, nume, x, y):
        self.nume = nume
        self.img = getColorImage("red")
        self.loc = self.img.get_rect()
        self.loc.center = x,y
        self.setDirection()
        self.color = None



    def setColor(self,clr):
        if clr == "red":
            self.img = pygame.image.load("sem_ros.png")
            self.color = "red"
        elif clr == "green":
            self.img = pygame.image.load("sem_verde.png")
            self.color = "green"
        self.setDirection()

    def setDirection(self):  #seteaza directia semaforului (cum e orientat)
        self.img = pygame.transform.scale(self.img, (25, 67))
        if self.nume == "sem_sus":
            self.img = pygame.transform.rotate(self.img, 180)
        elif self.nume == "sem_dr":
            self.img = pygame.transform.rotate(self.img, 90)
        elif self.nume == "sem_stg":
            self.img = pygame.transform.rotate(self.img, 270)
        elif self.nume == "sem_jos":
            self.img = self.img

    def getColor(self):
        return self.color




def getColorImage(color):  #obtine imaginea cu acea culoare
    if color == "red":
        return pygame.image.load("sem_ros.png")
    elif color == "green":
        return pygame.image.load("sem_verde.png")


