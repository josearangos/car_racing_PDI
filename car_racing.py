#----------Conceptos básicos de PDI----------------------------
#----------Por: Jose Alberto Arango Sánchez jose.arangos@udea.edu.co CC 1017246338 ----------------------------
#-----------Leon Dario Arango Amaya leon.arango@udea.edu.co CC        ----------------------------------------
#-----------Curso Básico de Procesamiento de Imágenes y Visión Artificial------------------------------------
#---------- 13 Abril de 2020 --------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
# 1. IMPORTANDO LAS LIBRERÍAS NECESARIAS
#--------------------------------------------------------------------------------------------------------------

import cv2 #Opencv
import numpy as  np #Numpy, usada para calculos matriciales
import pygame #Librería usada para crear el entorno de juego
import time #Librería usada para el manejo del tiempo
import random #Librería usada para generar valores random
import threading #Librería usada para el manejo de hilos
#--------------------------------------------------------------------------------------------------------------
# 2. INICIALIZAR LAS VARIABLES
#--------------------------------------------------------------------------------------------------------------
pygame.init() #Inicializamos la librería pygame
display_width = 800 #Dimensiones de campo de juego
display_height = 600 #Dimensiones de campo de juego
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
car_width = 50 #Dimension del carro
car_height = 100 #Dimensi
pygame.mixer.music.load("assets/Hurry_Up.mp3")


gameDisplay = pygame.display.set_mode((display_width, display_height)) #Definimos las dimensiones del lienzo de juego
pygame.display.set_caption("Car Racing") # Definimos el titulo de la ventana de juego
clock = pygame.time.Clock() #Creamos un objeto tipo reloj, para administrar los tiempos dentro del juego
carImg = pygame.image.load("assets/car3.png")  # cargamos los carros del juego
car2Img = pygame.image.load("assets/car2.png")  # cargamos los carros del juego
bgImg = pygame.image.load("assets/back2.jpg")  #Cargamos la pista de juego
bgImg2 = pygame.image.load("assets/back3.jpg") #Cargamos la pista de juego
crash_img = pygame.image.load("assets/crash.png")  # Imagen de crash
cap = cv2.VideoCapture(0) # Es la camara por defecto del ordenador.
cordeX, cordeY = 0, 0 #Coordenadas del objeto a detectar por su color
car_x_change = 0 #Dirección en la que se mueve el vehiculo deacuerdo a la pocision donde se encuentre
font = cv2.FONT_HERSHEY_SIMPLEX #tipo de fuente usada para el texto en la pantalla de la imagen
#--------------------------------------------------------------------------------------------------------------
# 3. MÉTODOS DE PDI
#--------------------------------------------------------------------------------------------------------------

# El siguiente método se encarga de graficar el punto medio donde se encuentra una bola de color azul la cual es la encargada de definir la dirección del carro
def pointCoordenates(frame):
    global cordeX, cordeY   #Coordenadas del objeto a detectar por su color
    #Definimos los rangos del color a detectar
    azulBajo = np.array([100, 100, 20])
    azulAlto = np.array([125, 255, 255])
    #Convertimos la imagen de BGR a HSV que es el modelo de coordenadas usado
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Aplicamos la mascara
    mask = cv2.inRange(frameHSV, azulBajo, azulAlto)
    # Obtenemos los contornos de las partes blancas y los dibujamos
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Como se dibujan multiples contornos, solo seleccionaremos los que cumplan cierta area.
    for contor in contornos: #Recorremos todos los contornos azules encontrados
        area = cv2.contourArea(contor) #Obtenemos el area de los contornos
        if area > 700: #Solo los mayores a 700
            # Buscamos las coordenadas del centro
            centros = cv2.moments(contor)
            if (centros["m00"] == 0): centros["m00"] = 1
            x = int(centros["m10"] / centros["m00"])
            y = int(centros["m01"] / centros["m00"])
            cordeX = x # coordenada x del contorno
            cordeY = y # coordenada y del contorno
            # Dibujamos un circulo con las coordenadas del contorno
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1) # 7 es el radio del circulo
            # Mostramos en pantalla las coordenadas
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            # Luego de eliminar los contorno menores a cierta area, vamos a suavizar los contornos
            contorSuavi = cv2.convexHull(contor) #suavizamos los contornos
            cv2.drawContours(frame, [contorSuavi], 0, (255, 0, 0), 3) #dibujamos los contornos

#El siguiente método se encarga de leer los frames de la camara y realizar el preprocesado para saber la dirección del carro
def openCamera():
    global car_x_change,cordeX,cordeY   #Coordenadas del objeto a detectar por su color

    while (cap.isOpened()): #Mientras la camara se encuentre abierta se realizará la lectura de los frames
        ret, frame = cap.read() # capturamos un frame
        frame = cv2.flip(frame, 1) #Usamos flip 1 para girar el frame horizontalmente
        if ret == True: # Si se logró leer con exito un frame realizamos el preprocesado.
            #Creamos el volante

            cv2.circle(frame,(318,382),170,(0,255,0),2)

            fil = frame.shape[0]  #capturamos las dimensiones de l frame
            col = frame.shape[1]  #capturamos las dimensiones de l frame
            # las coordenas en x de las lineas usadas para los umbrales
            x_medio_derecha = int((col + 60) / 2)
            x_medio_izquierda = int((col - 60) / 2)
            cordeX = int(col / 2) #inicializamos las cordenas de la bola
            cordeY = int(fil / 2) #inicializamos las cordenas de la bola
            # creamos dos lineas, las cuales nos servirán para definir los segmentos donde se encuentre la bola azul
            # Linea derecha
            cv2.line(frame, (x_medio_derecha, 0), (x_medio_derecha, fil), (0, 255, 0), 2)
            # Linea izquierda
            cv2.line(frame, (x_medio_izquierda, 0), (x_medio_izquierda, fil), (0, 255, 0), 2)
            pointCoordenates(frame) #Hacemos uso de la función documentada anteriormente
            # Deacuerdo a la coordenada en X donde se encuentre la bolita a detectar, realizamos el moviemto del vehiculo
            # izquierda
            if (cordeX > 0 and cordeX < x_medio_izquierda):
                car_x_change = -0.5 #indica que la bolita se encuentra en el segmento izquierdo y por lo tanto el usuario desea mover el vehiculo en esta dirección
            if (cordeX >= x_medio_izquierda and cordeX <= x_medio_derecha):
                car_x_change = 0 #indica que la bolita se encuentra en el segmento centro y por lo tanto el usuario desea no mover el vehiculo en ninguna dirección
            if (cordeX > x_medio_derecha and cordeX < col): #indica que la bolita se encuentra en el segmento derecho y por lo tanto el usuario desea mover el vehiculo en esta dirección
                car_x_change = 0.5
            cv2.imshow('Car_Racing_PDI', frame) #Mostramos la imagen
            if cv2.waitKey(1) & 0xFF == ord('s'): # Cuando se presione la tecla 'S', se cierra la pestaña
                break
    cap.release() #Finalizamos la lectura de la camara
    cv2.destroyAllWindows() #Destruimos las pestañas

#--------------------------------------------------------------------------------------------------------------
# 4. MÉTODOS DEL JUEGO
#--------------------------------------------------------------------------------------------------------------



def intro():
    intro = True
    menu1_x = 200
    menu1_y = 400
    menu2_x = 500
    menu2_y = 400
    menu_width = 100
    menu_height = 50
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.set_icon(carImg)

        pygame.draw.rect(gameDisplay, black, (200, 400, 100, 50))
        pygame.draw.rect(gameDisplay, black, (500, 400, 100, 50))

        gameDisplay.fill(white)
        message_display("CAR RACING", 100, display_width / 2, display_height / 2)
        gameDisplay.blit(carImg, ((display_width / 2) - 100, 10))
        pygame.draw.rect(gameDisplay, green, (200, 400, 100, 50))
        pygame.draw.rect(gameDisplay, red, (500, 400, 100, 50))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if menu1_x < mouse[0] < menu1_x + menu_width and menu1_y < mouse[1] < menu1_y + menu_height:
            pygame.draw.rect(gameDisplay, blue, (200, 400, 100, 50))
            if click[0] == 1:
                intro = False
        if menu2_x < mouse[0] < menu2_x + menu_width and menu2_y < mouse[1] < menu2_y + menu_height:
            pygame.draw.rect(gameDisplay, blue, (500, 400, 100, 50))
            if click[0] == 1:
                pygame.quit()
                quit()

        message_display("Go", 40, menu1_x + menu_width / 2, menu1_y + menu_height / 2)
        message_display("Exit", 40, menu2_x + menu_width / 2, menu2_y + menu_height / 2)
        pygame.display.update()
        clock.tick(50)
# This function update the score
def highscore(count):
    font = pygame.font.SysFont(None, 60)
    text = font.render("Score : " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def try_again_counter(count, score):
    # Try Again Timer
    font = pygame.font.SysFont(None, 250)
    text = font.render(str(count), True, black)
    gameDisplay.blit(text, (350, 250))

    # Final Score
    font = pygame.font.SysFont(None, 115)
    text = font.render("Score : " + str(score), True, black)
    gameDisplay.blit(text, (165, 170))


# This function print obstacle cars
def draw_things(thingx, thingy, thing):
    gameDisplay.blit(thing, (thingx, thingy))


# This function print our car
def car(x, y):
    gameDisplay.blit(carImg, (x, y))


# this function make the rectangles for buttons from initial menu
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


# This functio print buttons
def message_display(text, size, x, y):
    font = pygame.font.Font("assets/CaviarDreams.ttf", size)
    text_surface, text_rectangle = text_objects(text, font)
    text_rectangle.center = (x, y)
    gameDisplay.blit(text_surface, text_rectangle)

def crash(x,y,score):
    reset = 3
    #Stop Music
    #this put the crach img in the cash car position
    gameDisplay.blit(crash_img,(x,y))
    # Put Message, update display, and wait
    message_display("You Crashed",115,display_width/2,display_height/2)
    pygame.display.update()
    time.sleep(3)
    while reset > -1:
        gameDisplay.fill(white)
        try_again_counter(reset,score)
        time.sleep(1)
        reset-=1
        pygame.display.update()
    intro()
    gameloop() #for restart the game

def gameloop():
    global car_x_change
    pygame.mixer.stop()
    pygame.mixer.music.play(-1)
    bg_x1 = 0
    bg_x2 = 0
    bg_y1 = 0
    bg_y2 = -600
    bg_speed = 6
    bg_speed_change = 0
    car_x = ((display_width / 2) - (car_width / 2))
    car_y = (display_height - car_height)
    car_x_change = 0
    road_start_x = (display_width / 2) - 112
    road_end_x = (display_width / 2) + 112

    thing_startx = random.randrange(road_start_x, road_end_x - car_width)
    thing_starty = -600
    thingw = 50
    thingh = 100
    thing_speed = 1
    count = 0
    pause = False
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Here we can put the camera results
                if event.key == pygame.K_LEFT:
                    car_x_change = -1.5
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 1.5
                elif event.key == pygame.K_SPACE:
                    pause = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0

        while pause == True:
            message_display("Game Paused",115,display_width/2,display_height/2)
            pygame.display.update()
            time.sleep(0.5)
            gameDisplay.blit(bgImg, (bg_x1, bg_y1))
            gameDisplay.blit(bgImg2, (bg_x2, bg_y2))
            car(car_x, car_y)  # display car
            draw_things(thing_startx, thing_starty, car2Img)
            highscore(count)
            pygame.display.update()
            time.sleep(0.5)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Continue...")
                        pause = False
                        

        car_x += car_x_change

        if car_x > road_end_x - car_width:
            crash(car_x, car_y, count)
        if car_x < road_start_x:
            crash(car_x - car_width, car_y, count)

        if car_y < thing_starty + thingh - 25:
            if car_x >= thing_startx + 10 and car_x <= thing_startx + thingw - 10:
                # Left Crash
                crash(car_x - 25, car_y - car_height / 2, count)
            if car_x + car_width >= thing_startx - 10 and car_x + car_width <= thing_startx + thingw + 10:
                # Right Crash
                crash(car_x, car_y - car_height / 2, count)

        gameDisplay.blit(bgImg, (bg_x1, bg_y1))
        gameDisplay.blit(bgImg2, (bg_x2, bg_y2))

        car(car_x, car_y)  # display car
        draw_things(thing_startx, thing_starty, car2Img)
        highscore(count)
        count += 1

        # Update Speed Obstacle Cars
        thing_speed += 0.000
        thing_starty += thing_speed

        if thing_starty > display_height:
            thing_startx = random.randrange(road_start_x, road_end_x - car_width)
            thing_starty = -200

        bg_y1 += bg_speed
        bg_y2 += bg_speed

        if bg_y1 >= display_height:
            bg_y1 = -600

        if bg_y2 >= display_height:
            bg_y2 = -600
        #camera()
        pygame.display.update()  # update the screen
        clock.tick(128)  # frame per sec

#--------------------------------------------------------------------------------------------------------------
# . HILOS
#--------------------------------------------------------------------------------------------------------------
#Debido a que la camara debe funcionar de manera independiente se creo un hilo para tal fin usando la librería mencionada anteriormente
threadCamera = threading.Thread(target=openCamera)
threadCamera.start()

