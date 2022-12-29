
class CarQueue:
    def __init__(self, priority, direction, amount,carlist):
        self.carlist = carlist
        self.priority = priority
        self.direction = direction
        self.amount = amount
    def addCar(self, car):
        self.carlist.append(car)
        self.amount += 1

class CarQueues:
    def __init__(self):
        self.QUp = []   #up e directia in care merg deci sunt masinile care vin de jos
        self.QDown = []
        self.QLeft = []
        self.QRight = []
    def addCarQueue(self, c, direction):
        if direction == "Up":
            self.QUp.append(c)
        elif direction == "Down":
            self.QDown.append(c)
        elif direction == "Left":
            self.QLeft.append(c)
        elif direction == "Right":
            self.QRight.append(c)
