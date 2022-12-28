import pygame
from pygame.locals import *
from car import Car
from semafoare import Semafor
from time import sleep
from threading import Timer


#timer:
# timp =0
# def incr_time():
#     global timp
#     timp+=1
#     print(timp)

#primul argument zice din cate in cate secunde sa se apeleze incr_timer
# timer = RepeatedTimer(0.5,incr_time) # it auto-starts, no need of rt.start()
########
############################
# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer     = None
#         self.interval   = interval
#         self.function   = function
#         self.args       = args
#         self.kwargs     = kwargs
#         self.is_running = False
#         self.start()
#
#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)
#
#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True
#
#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False

#https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
##########################

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

# car1 = Car("masina-removebg-preview.png", coordDOWN, "up")
# car2 = Car("masina-removebg-preview.png", coordUP, "down")
# car3 = Car("masina-removebg-preview.png", coordLEFT, "right")
# car4 = Car("masina-removebg-preview.png", coordRIGHT, "left")


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
    elif isInside(pos,25, height / 2 + road_width-25, 50,50): #butonul din stg
        if(k-k_buton_stg)>DELAY:
            k_buton_stg=k
            nrCars_stg += 1
            caraux = Car("masina-removebg-preview.png", coordLEFT, "right", nrCars_stg)
            carList.append(caraux)
            carListAux.append(caraux)
    elif isInside(pos,width/2 + road_width-25, height - 75, 50, 50): #butonul de jos
        if(k-k_buton_sus)>DELAY:
            k_buton_sus=k
            nrCars_jos += 1
            caraux = Car("masina-removebg-preview.png", coordDOWN, "up", nrCars_jos)
            carList.append(caraux)
            carListAux.append(caraux)
    elif isInside(pos,width/2- road_width-25, 25,50,50): #butonul de sus
        if(k-k_buton_jos)>DELAY:
            k_buton_jos=k
            nrCars_sus += 1
            caraux = Car("masina-removebg-preview.png", coordUP, "down", nrCars_sus)
            carList.append(caraux)
            carListAux.append(caraux)

#scoatem masina daca a trecut de mijloc plus 50 px crd
def passed(c):
    return c.hasPassed()

# pt fiecare directie de mers verificam sa fie inainte de inceputul intersectiei pt a adauga acea masina in coada acelei directii si comparam lungimea cozilor si
# punem verde la cea mai lunga coada si rosu la cealalta
#actually cred ca ar trb sa luam in calcul si partea opusa de drum pt ca verde e pt ambele parti
#daca este o coada mai mica, care ar trece prin intersectie inainte ca marea coada sa ajunga la intersectie, ii afisam acesteia verde (finalul cozii mici sa mai aproape de trecerea intersectiei
#decat inceputul cozii mari de inceputul intersectiei@@@@@@@@@@@@@!! (important)
##################ALGORITM
def controlSemafoare():
    nr_up_down = 0
    nr_left_right=0
    for c in carList:
        if c.direction == "up" or c.direction =="down":
            nr_up_down += 1
        else:
            nr_left_right += 1
    if nr_up_down > nr_left_right:
        sem_sus.setColor("green")
        sem_jos.setColor("green")
        sem_dr.setColor("red")
        sem_stg.setColor("red")
    else:
        sem_dr.setColor("green")
        sem_stg.setColor("green")
        sem_sus.setColor("red")
        sem_jos.setColor("red")


def manageCar(c):  #if c has passed manage it
    global nrCars_jos, nrCars_sus, nrCars_stg, nrCars_dr
    if c.direction == "up":
          nrCars_jos -= 1
    elif c.direction == "down":
          nrCars_sus -= 1
    elif c.direction == "left":
          nrCars_dr -= 1
    else:
          nrCars_stg -= 1
    carList.remove(c)





k=0
while running:
    #animatie vehicul
    controlSemafoare()
    if(k%1000==0):
        print("nrCars_jos: ", nrCars_jos, "nrCars_sus: ", nrCars_sus, "nrCars_stg: ", nrCars_stg, "nrCars_dr: ", nrCars_dr)

    k+=1
    if k%8==0:

        for c in carListAux:
            c.move(c.direction, sem_dr.getColor(), sem_stg.getColor(), sem_sus.getColor(), sem_jos.getColor(),
                   nrCars_dr, nrCars_stg, nrCars_sus, nrCars_jos, passed(c))
            #daca a trecut de mijloc + latura patratului din mijloc, scoatem din lista
            # if(passed(c)):
            #     print("car with index ", c.index, " has passed")
            #     #carList.remove(c)
            #     manageCar(c)
        for c in carList:  # acest loop e necesar pt ca dupa ce dau remove din carList, in carlistaux tot ramane masina deci da crash cand dau remove
            if(passed(c)):
                print("car with index ", c.index, " has passed")
                manageCar(c)


    for event in pygame.event.get(): # in pygame.event se afla toate evenimentele din app
        if event.type == QUIT:  #event listener pt quit (apasare pe X)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            leftClick = pygame.mouse.get_pressed(num_buttons=3)[0]
            handleClick(k, pygame.mouse.get_pos())

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

