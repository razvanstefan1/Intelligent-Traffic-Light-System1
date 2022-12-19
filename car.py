import pygame

class Car:
    def __init__(self, img, startxy, direction, index):
        self.img = pygame.image.load(img)
        self.startx = startxy[0]
        self.starty = startxy[1]
        self.car_loc = self.img.get_rect()
        self.car_loc.center = startxy[0], startxy[1]
        self.direction = direction
        self.index=index  #index ul masinii dintre masinile de pe directia aceea (4 directii); folosim pt coliziuni intre masini
        self.scale_rotate()

    def draw(self, screen):
        screen.blit(self.img, self.car_loc)

    #move doar daca nu e masina in fata sau nu e rosu in fata
    def move(self, direction, culoare_dr,culoare_st,culoare_sus,culoare_jos,nrDr,nrSt,nrSus,nrJos):
        if direction == "up" and (culoare_jos != "red" or self.car_loc[1] > 400 + 38 * self.index ): #38 e lungimea masinii si nrjos e indexul masinii dintre cele de jos
            self.car_loc[1] -= 1
        elif direction == "down" and (culoare_sus != "red" or self.car_loc[1] < 400  - 38 * self.index):  #initial era 400-76 dar am modificat
            self.car_loc[1] += 1
        elif direction == "right" and (culoare_st != "red" or self.car_loc[0] < 800 - 38 - 38 * self.index):
            self.car_loc[0] += 1
        elif direction == "left" and (culoare_dr != "red" or self.car_loc[0] > 800 + 38 * self.index):
            self.car_loc[0] -= 1

    def hasPassed(self):
        if self.direction == "up" and self.car_loc[1] <320:
            return True
        if self.direction == "down" and self.car_loc[1] > 440:
            return True
        if self.direction == "right" and self.car_loc[0] > 840:
            return True
        if self.direction == "left" and self.car_loc[0] < 720:
            return True
        return False

    def scale_rotate(self):
        self.img = pygame.transform.scale(self.img, (25, 38))
        if self.direction == "up":
            pass

        if self.direction == "down":
            self.img = pygame.transform.rotate(self.img, 180)

        if self.direction == "right":
            self.img = pygame.transform.rotate(self.img, 270)

        if self.direction == "left":
            self.img = pygame.transform.rotate(self.img, 90)
