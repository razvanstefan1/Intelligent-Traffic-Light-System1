
class CarQueue:
    def __init__(self, priority, direction, amount):
        self.carlist = []
        self.priority = priority
        self.direction = direction
        self.amount = amount
        self.lastCar = None
        self.firstCar = None
        self.dist_head_inceput = 0 # distanta dintre inceputul primei masini la inceputul intersectiei
        self.dist_tail_sfarsit=0 # distanta dintre sf ultimei masini la sfarsitul intersectiei
    def addCar(self, car):
        self.carlist.append(car)
        self.amount += 1
        if self.amount == 1:
            self.firstCar = car
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

    def updatePriorities(self,k):
        self.calculateDistances()
        nrsusjos=0
        nrdrst=0
        distsusjos_inceput=0
        distsusjos_sfarsit=0
        distdrst_inceput=0
        distdrst_sfarsit=0
        for c in self.QUp:
            nrsusjos += c.amount
            distsusjos_inceput += c.dist_head_inceput
            distsusjos_sfarsit += c.dist_tail_sfarsit
        for c in self.QDown:
            nrsusjos += c.amount
            distsusjos_inceput += c.dist_head_inceput
            distsusjos_sfarsit += c.dist_tail_sfarsit
        for c in self.QLeft:
            nrdrst+=c.amount
            distdrst_inceput += c.dist_head_inceput
            distdrst_sfarsit += c.dist_tail_sfarsit
        for c in self.QRight:
            nrdrst+=c.amount
            distdrst_inceput += c.dist_head_inceput
            distdrst_sfarsit += c.dist_tail_sfarsit


        if(nrsusjos==0):
            self.QLeft[0].priority = 1000
            self.QRight[0].priority = 999
            self.QDown[0].priority = 1
            self.QUp[0].priority = 0
            if(k%400==0):
             print (1)

        elif(nrdrst==0):
            self.QUp[0].priority = 1000
            self.QDown[0].priority = 999
            self.QLeft[0].priority = 1
            self.QRight[0].priority = 0
            if (k % 400 == 0):
             print (2)
        elif(nrsusjos == nrdrst):
            if(distdrst_inceput <= distsusjos_inceput):
                self.QLeft[0].priority = 1000
                self.QRight[0].priority = 999
                self.QDown[0].priority = 1
                self.QUp[0].priority = 0
                if(k%400==0):
                 print (distdrst_inceput, distsusjos_inceput, 3)
            else:
                self.QLeft[0].priority = 0
                self.QRight[0].priority = 1
                self.QDown[0].priority = 1000
                self.QUp[0].priority = 999
                if(k%400==0):
                 print (distdrst_inceput, distsusjos_inceput, 4)
        elif(nrsusjos > nrdrst):
            if(distsusjos_inceput <= distdrst_sfarsit):
                self.QLeft[0].priority = 0
                self.QRight[0].priority = 1
                self.QDown[0].priority = 1000
                self.QUp[0].priority = 999
                if(k%400==0):
                 print (5)
            else:
                self.QLeft[0].priority = 1000
                self.QRight[0].priority = 999
                self.QDown[0].priority = 1
                self.QUp[0].priority = 0
                if(k%400==0):
                 print (6)
        elif(nrsusjos<=nrdrst):
            if(distdrst_inceput <= distsusjos_sfarsit):
                self.QLeft[0].priority = 1000
                self.QRight[0].priority = 999
                self.QDown[0].priority = 1
                self.QUp[0].priority = 0
                if(k%400==0):
                 print (7)
            else:
                self.QLeft[0].priority = 0
                self.QRight[0].priority = 1
                self.QDown[0].priority = 1000
                self.QUp[0].priority = 999
                if(k%400==0):
                 print (8)





        # for queues in self.allQueues:
        #     for carlist in queues:
        #         carlist.priority = carlist.amount #provizoriu

    def calculateDistances(self):
        for c in self.QUp:
          if(c.firstCar!= None):
            c.dist_head_inceput = c.firstCar.car_loc[1] - 440
            c.dist_tail_sfarsit = c.lastCar.car_loc[1] + 38 - 359
        for c in self.QDown:
          if (c.firstCar != None):
            c.dist_head_inceput = 359 - c.firstCar.car_loc[1] + 38
            c.dist_tail_sfarsit = 440 - c.lastCar.car_loc[1]
        for c in self.QLeft:
          if (c.firstCar != None):
            c.dist_head_inceput = c.firstCar.car_loc[0] - 840
            c.dist_tail_sfarsit = c.lastCar.car_loc[0] + 38 - 759
        for c in self.QRight:
          if (c.firstCar != None):
            c.dist_head_inceput = 759 - c.firstCar.car_loc[0] + 38
            c.dist_tail_sfarsit = 840 - c.lastCar.car_loc[0]
        return 0

