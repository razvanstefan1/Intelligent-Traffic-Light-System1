
class CarQueue:
    def __init__(self, priority, direction, amount):
        self.carlist = []
        self.priority = priority
        self.direction = direction
        self.amount = amount
        self.lastCar = None
    def addCar(self, car):
        self.carlist.append(car)
        self.amount += 1
        self.lastCar = car #ultima masina din coada
    def removeCar(self, car):
        if(car == self.lastCar):
            self.amount = 0  #daca a trecut ultima masina atunci golim coada
        self.carlist.remove(car)
        #self.amount -= 1


class CarQueues:
    def __init__(self):
        self.QUp = []   #up e directia in care merg deci sunt masinile care vin de jos
        self.QDown = []
        self.QLeft = []
        self.QRight = []
        self.allQueues = [self.QUp, self.QDown, self.QLeft, self.QRight]
    def addCarQueue(self, c, direction):
        if direction == "Up":
            self.QUp.append(c)
        elif direction == "Down":
            self.QDown.append(c)
        elif direction == "Left":
            self.QLeft.append(c)
        elif direction == "Right":
            self.QRight.append(c)
    def getMaxPriorityDirection(self):  #returneaza lista cu prioritate maxima
        max = 0
        aux = " "
        for queues in self.allQueues:
            for carlist in queues:
                if carlist.priority >= max:
                    max = carlist.priority
                    aux = carlist.direction
        return aux

    def updatePriorities(self):
        for queues in self.allQueues:
            for carlist in queues:
                carlist.priority = carlist.amount #provizoriu

