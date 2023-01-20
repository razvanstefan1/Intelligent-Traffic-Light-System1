import pygame
from pygame.locals import *
from car import Car
from semafoare import Semafor
from carqueue import CarQueue, CarQueues


size = width, height = (1600,800) #screen size
road_width = width/20 #width of the road
carList = []    #carList contine lista masinilor care nu au trecut drumul
carListAux = [] #carListAux contine toate masinile, si cele care au trecut drumul. Se foloseste pentru a desena masinile si dupa
#ce trec (ca sa nu dispara dupa ce trec)
pygame.init()

running = True
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Simulare trafic")  # Title of the window
screen.fill((0, 102, 0))  # fill the screen with green (culoare fundal)


#create first car
coordDOWN =(width/2 + 28, 750)  #coordonatele masinii ce incepe jos
coordUP =(width/2 - 15, 50)
coordLEFT =(50, height/2 + 48)
coordRIGHT =(width-50, height/2 + 5)

def draw_buttons():
    buton1 = pygame.image.load("buton1.png")
    buton_loc = buton1.get_rect()
    buton_loc.center = (width- 50, height/2 -road_width)  #dr
    screen.blit(buton1, buton_loc)
    buton_loc.center = (50, height / 2 + road_width)  #stg
    screen.blit(buton1, buton_loc)
    buton_loc.center = (width/2 + road_width, height - 50)  #jos
    screen.blit(buton1, buton_loc)
    buton_loc.center = (width/2- road_width, 50)   #sus
    screen.blit(buton1, buton_loc)

#semafoare
sem_dr = Semafor("sem_dr", width/2 + 70, height / 2 -12)
sem_stg = Semafor("sem_stg", width/2 - 85, height / 2 +road_width + 20)
sem_jos = Semafor("sem_jos",width/2 + road_width-10 , height/2 + 100)
sem_sus = Semafor("sem_sus",width/2 - road_width + 35, height/2 - 50)


def draw_lines(x,y,width,height,gap,horizontal):
    if horizontal:
        i=0
        while(i+width<size[0]): #draw lines until the end of the screen
            pygame.draw.rect(screen,(255,255,255),(i,y,width,height))
            i+=width+gap
    else:
        i=10
        while(i+height<size[1]):
            pygame.draw.rect(screen,(255,255,255),(x,i,width,height))
            i+=height+gap

def isInside(pos, x, y, width, height):
    if pos[0] > x and pos[0] < x + width:
        if pos[1] > y and pos[1] < y + height:
            print("inside")
            return True
    return False


#variabile pentru a retine ultima apasare a butonului (pt a controla coliziunile)
k_buton_sus=0
k_buton_jos=0
k_buton_stg=0
k_buton_dr=0
DELAY=300 #delay pt a nu se inregistra clickuri care daca ar fi apasate asa des, s ar suprapune masinile
#variabile pt a retine nr de masini de pe fiecare sens ca sa calculez unde sa se opreasca fiecare daca e rosu
#astfel incat sa nu se suprapuna
nrCars_jos=0  #nr cars e nr de masini si index ul (dar indexam de la 1) nrcarsjos e cate masini pleaca de jos
nrCars_sus=0
nrCars_stg=0
nrCars_dr=0


###############################CAR QUEUE
QJos = CarQueue(0,"Down", 0)
QSus = CarQueue(0,"Up", 0)
QStg = CarQueue(0,"Left", 0)
QDr = CarQueue(0,"Right", 0)
carQueues = CarQueues()
carQueues.addCarQueue(QJos, "Down")  #adaugam coada Qjos la lista cozilor de jos din carQueues
carQueues.addCarQueue(QSus, "Up")
carQueues.addCarQueue(QStg, "Left")
carQueues.addCarQueue(QDr, "Right")

#aici pun masinile care nu au fost adaugate la queue inca
QJosLateArrivals = CarQueue(0,"Down", 0)
QSusLateArrivals = CarQueue(0,"Up", 0)
QStgLateArrivals = CarQueue(0,"Left", 0)
QDrLateArrivals = CarQueue(0,"Right", 0)
###############################CAR QUEUE


#draw cars at click
def handleClick(k, pos):
    global k_buton_sus, k_buton_jos, k_buton_stg, k_buton_dr # sa modific var globala, nu locala
    global nrCars_jos, nrCars_sus, nrCars_stg, nrCars_dr
    print ("click at " , pos )
    if isInside(pos, width- 75, height/2 -road_width-25, 50, 50 ): # butonul din dr
        if (k-k_buton_dr)>DELAY:
            k_buton_dr=k
            nrCars_dr += 1
            caraux = Car("masina-removebg-preview.png", coordRIGHT, "left", nrCars_dr)
            carList.append(caraux)
            carListAux.append(caraux)
            if not QStg.addCar(caraux):
                QStgLateArrivals.carlist.append(caraux)
    elif isInside(pos,25, height / 2 + road_width-25, 50,50): #butonul din stg
        if(k-k_buton_stg)>DELAY:
            k_buton_stg=k
            nrCars_stg += 1
            caraux = Car("masina-removebg-preview.png", coordLEFT, "right", nrCars_stg)
            carList.append(caraux)
            carListAux.append(caraux)
            if not QDr.addCar(caraux):
                QDrLateArrivals.carlist.append(caraux) #nu folosim carList ca sa nu se tot apeleze aia
    elif isInside(pos,width/2 + road_width-25, height - 75, 50, 50): #butonul de jos
        if(k-k_buton_sus)>DELAY:
            k_buton_sus=k
            nrCars_jos += 1
            caraux = Car("masina-removebg-preview.png", coordDOWN, "up", nrCars_jos)
            carList.append(caraux)
            carListAux.append(caraux)
            if not QSus.addCar(caraux):
                QSusLateArrivals.carlist.append(caraux)
    elif isInside(pos,width/2- road_width-25, 25,50,50): #butonul de sus
        if(k-k_buton_jos)>DELAY:
            k_buton_jos=k
            nrCars_sus += 1
            caraux = Car("masina-removebg-preview.png", coordUP, "down", nrCars_sus)
            carList.append(caraux)
            carListAux.append(caraux)
            if not QJos.addCar(caraux):
                QJosLateArrivals.carlist.append(caraux)

#scoatem masina daca a trecut de mijloc plus 50 px crd
def passed(c):
    return c.hasPassed()

def manageLateArrivals():
    global QJosLateArrivals, QSusLateArrivals, QStgLateArrivals, QDrLateArrivals
    if len(QJosLateArrivals.carlist) > 0:
        if QJos.addCar(QJosLateArrivals.carlist[0]):
            QJosLateArrivals.carlist.pop(0)
    if len(QSusLateArrivals.carlist) > 0:
        if QSus.addCar(QSusLateArrivals.carlist[0]):
            QSusLateArrivals.carlist.pop(0)
    if len(QStgLateArrivals.carlist) > 0:
        if QStg.addCar(QStgLateArrivals.carlist[0]):
            QStgLateArrivals.carlist.pop(0)

def middleClear(): #true daca nu sunt masini in mijlocul intersectiei
    global carList
    #!!!!!!!!!!!!!!car_loc returneaza mereu coord punctului din stanga sus oricum ar fi orientata masina (adica coltul cel mai aproape de coltul stg sus al ecranului)
    for c in carList:
        if c.direction == "down":
            x = c.car_loc[0]
            y = c.car_loc[1] + 38   # 38 e lungimea masinii
        if c.direction == "right":
            x = c.car_loc[0] + 38
            y = c.car_loc[1]
        else:
            x = c.car_loc[0]
            y = c.car_loc[1]

        if 759 <= x <= 840 and 359 <= y <=440:
            return False
    return True


def controlSemafoare(k):
    global carQueues
    global QJos, QSus, QStg, QDr
    carQueues.updatePriorities(k)

    manageLateArrivals()

    aux = carQueues.getMaxPriorityDirection()
    #print (aux + " is the max priority direction")
    if aux in ["Down", "Up"] and middleClear() :
        sem_sus.setColor("green")
        sem_jos.setColor("green")
        sem_dr.setColor("red")
        sem_stg.setColor("red")
    elif aux in ["Left", "Right"]:
        sem_sus.setColor("red")
        sem_jos.setColor("red")
        sem_dr.setColor("green")
        sem_stg.setColor("green")


def manageCar(c):  #if c has passed manage it
    global nrCars_jos, nrCars_sus, nrCars_stg, nrCars_dr
    if c.direction == "up":
          nrCars_jos -= 1
          for carq in carQueues.QUp: #parcurgem cozile cu directia up din carQueues si scoatem c din lista in care este
              if c in carq.carlist:
                  carq.removeCar(c) #dar amount ul cozii se goleste doar cand trece ultima masina din coada
                                    #astfel se evita acele ciocniri si alternari rapide rosu verde

    elif c.direction == "down":
          nrCars_sus -= 1
          for carq in carQueues.QDown:
              if c in carq.carlist:
                  carq.removeCar(c)

    elif c.direction == "left":
          nrCars_dr -= 1
          for carq in carQueues.QLeft:
              if c in carq.carlist:
                  carq.removeCar(c)
    else:
          for carq in carQueues.QRight:
                if c in carq.carlist:
                    carq.removeCar(c)
          nrCars_stg -= 1
    carList.remove(c)



k=0
while running:
    controlSemafoare(k)
    k+=1
    if k%7==0:
        for c in carListAux:
            c.move(c.direction, sem_dr.getColor(), sem_stg.getColor(), sem_sus.getColor(), sem_jos.getColor(),
                   nrCars_dr, nrCars_stg, nrCars_sus, nrCars_jos, passed(c))
        for c in carList:  # acest loop e necesar pt ca dupa ce dau remove din carList, in carlistaux tot ramane masina deci da crash cand dau remove
            if(passed(c)):
                manageCar(c)


    for event in pygame.event.get(): # in pygame.event se afla toate evenimentele din app
        if event.type == QUIT:  #event listener pt quit (apasare pe X)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            leftClick = pygame.mouse.get_pressed(num_buttons=3)[0]
            handleClick(k, pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                handleClick(k, (720,50))  # !!!!!!!!!!!!!! DACA APAS TASTA SUS O TRATEZ CA PE UN CLICK PE BUTONUL DE SUS (TUPLA DATA CA PARAMETRU E IN INTERIORUL BUTONULUI)
            if event.key == pygame.K_DOWN:
                handleClick(k, (878,740))
            if event.key == pygame.K_LEFT:
                handleClick(k, (52,488))
            if event.key == pygame.K_RIGHT:
                handleClick(k, (1556,320))

    #draw road
    pygame.draw.rect(screen, (50, 50, 50), (int(width / 2 - road_width / 2), 0, road_width, height))
    pygame.draw.rect(screen, (50, 50, 50), (0, int(height / 2 - road_width / 2), width, road_width))
    #draw lines
    draw_lines(0,size[1]/2-3,50, 6, 20, True)
    draw_lines(size[0]/2-3,800,6,50,20, False) #vertical
    pygame.draw.rect(screen,(50,50,50),(int(width / 2 - road_width / 2),int(height / 2 - road_width / 2), road_width, road_width) )

    #desenarea masinilor
    for c in carListAux:
        c.draw(screen)

    #desenarea butoanelor
    draw_buttons()
    #desenare semafoare
    screen.blit(sem_dr.img,  sem_dr.loc)
    screen.blit(sem_stg.img, sem_stg.loc)
    screen.blit(sem_jos.img, sem_jos.loc)
    screen.blit(sem_sus.img, sem_sus.loc)
    pygame.display.update()  # update the screen
pygame.quit()

