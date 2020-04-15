#----------Conceptos básicos de PDI----------------------------
#----------Por: Jose Alberto Arango Sánchez jose.arangos@udea.edu.co CC 1017246338 --------------------------
#-----------Leon Dario Arango Amaya leon.arango@udea.edu.co CC 1044507887 -----------------------------------
#-----------Curso de Procesamiento Digital de Imágenes ------------------------------------------------------
#---------- 13 Abril de 2020 --------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------
# 1. IMPORTANDO LAS LIBRERÍAS NECESARIAS
#------------------------------------------------------------------------------------------------------------

import cv2 #Opencv
import numpy as  np #Numpy, usada para calculos matriciales
import pygame #Librería usada para crear el entorno de juego
import time #Librería usada para el manejo del tiempo
import random #Librería usada para generar valores random
import threading #Librería usada para el manejo de hilos
#-----------------------------------------------------------------------------------------------------------
# 2. INICIALIZAR LAS VARIABLES
#-----------------------------------------------------------------------------------------------------------
pygame.init() #Inicializamos la librería pygame
display_width = 800 #Dimensiones de campo de juego
display_height = 600 #Dimensiones de campo de juego
black = (0, 0, 0)
white = (255, 255, 255)
green = (44, 215, 223)
red = (255, 67, 34)
blue = (77, 77, 77)
car_width = 50 #Dimension del carro
car_height = 100 #Dimension del carro
crash_sound = pygame.mixer.Sound("./assets/crash.wav")
intro_sound = pygame.mixer.Sound("./assets/intro.wav")
start_sound = pygame.mixer.Sound("./assets/start.wav")



gameDisplay = pygame.display.set_mode((display_width, display_height)) #Definimos las dimensiones del lienzo de juego
pygame.display.set_caption("Car Racing") # Definimos el titulo de la ventana de juego
clock = pygame.time.Clock() #Creamos un objeto tipo reloj, para administrar los tiempos dentro del juego
carImg = pygame.image.load("./assets/car3.png")  # cargamos los carros del juego
car2Img = pygame.image.load("./assets/car2.png")  # cargamos los carros del juego
bgImg = pygame.image.load("./assets/back2.jpg")  #Cargamos la pista de juego
bgImg2 = pygame.image.load("./assets/back3.jpg") #Cargamos la pista de juego
crash_img = pygame.image.load("./assets/crash.png")  # Imagen de crash
background = pygame.image.load("./assets/Background.jpg")  # Imagen de crash
cap = cv2.VideoCapture(2) # Es la camara por defecto del ordenador.
cordeX, cordeY = 0, 0 #Coordenadas del objeto a detectar por su color
car_x_change = 0 #Dirección en la que se mueve el vehiculo deacuerdo a la pocision donde se encuentre
font = cv2.FONT_HERSHEY_SIMPLEX #tipo de fuente usada para el texto en la pantalla de la imagen
#-----------------------------------------------------------------------------------------------------------
# 3. MÉTODOS DE PDI
#-----------------------------------------------------------------------------------------------------------

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
                car_x_change = -0.7 #indica que la bolita se encuentra en el segmento izquierdo y por lo tanto el usuario desea mover el vehiculo en esta dirección
            if (cordeX >= x_medio_izquierda and cordeX <= x_medio_derecha):
                car_x_change = 0 #indica que la bolita se encuentra en el segmento centro y por lo tanto el usuario desea no mover el vehiculo en ninguna dirección
            if (cordeX > x_medio_derecha and cordeX < col): #indica que la bolita se encuentra en el segmento derecho y por lo tanto el usuario desea mover el vehiculo en esta dirección
                car_x_change = 0.7
            cv2.imshow('Car_Racing_PDI', frame) #Mostramos la imagen
            if cv2.waitKey(1) & 0xFF == ord('s'): # Cuando se presione la tecla 'S', se cierra la pestaña
                break
    cap.release() #Finalizamos la lectura de la camara
    cv2.destroyAllWindows() #Destruimos las pestañas

#-----------------------------------------------------------------------------------------------------------
# 4. MÉTODOS DEL JUEGO
#-----------------------------------------------------------------------------------------------------------


#El siguiente método se renderiza la ventana inicial del juego, la cúal contiene el menú.
def intro():
    pygame.mixer.Sound.play(intro_sound) #Iniciamos la música
    intro_sound.set_volume(0.1) #Control de volumen
    intro = True #variable para identificar que debe renderizar el menu
    #Variables para los botones del menu
    menu1_x = 200
    menu1_y = 400
    menu2_x = 500
    menu2_y = 400
    menu_width = 100
    menu_height = 50

    #Ciclo para mantener abierto el menu
    while intro:
        for event in pygame.event.get(): #Listener de pygame para eventos
            if event.type == pygame.QUIT: #Opción para salir
                pygame.quit()
                quit()
        pygame.display.set_icon(carImg) #Icono del juego

        gameDisplay.blit(background, (0, 0)) #Imagen de fondo 
        pygame.draw.rect(gameDisplay, green, (200, 400, 100, 50)) #Rectangulo boton
        pygame.draw.rect(gameDisplay, red, (500, 400, 100, 50)) #Rectangulo boton

        mouse = pygame.mouse.get_pos() #listener mouse
        click = pygame.mouse.get_pressed() #listener click

        if menu1_x < mouse[0] < menu1_x + menu_width and menu1_y < mouse[1] < menu1_y + menu_height:
            pygame.draw.rect(gameDisplay, blue, (200, 400, 100, 50))
            if click[0] == 1: #Si ocurre este evento, iniciara el juego
                pygame.mixer.Sound.stop(intro_sound)
                intro = False
        if menu2_x < mouse[0] < menu2_x + menu_width and menu2_y < mouse[1] < menu2_y + menu_height:
            pygame.draw.rect(gameDisplay, blue, (500, 400, 100, 50))
            if click[0] == 1: #Si ocurre este evento cerrara el juego
                pygame.quit()
                quit()

        message_display("Start", 40, menu1_x + menu_width / 2, menu1_y + menu_height / 2) #Texto del boton del juego
        message_display("Exit", 40, menu2_x + menu_width / 2, menu2_y + menu_height / 2) #Texto del boton de salir
        pygame.display.update() #Esta linea la veremos multiples veces, lo hace es renderizar el contenido e la ventana
        clock.tick(50) #Control de frames

# This function update the score
def highscore(count):
    font = pygame.font.SysFont(None, 60) #Tamaño de Fuente
    text = font.render("Score : " + str(count), True, black)#Texto
    gameDisplay.blit(text, (0, 0)) #Renderizado 


def try_again_counter(count, score):
    # Try Again Timer
    font = pygame.font.SysFont(None, 250) #Tamaño de Fuente
    text = font.render(str(count), True, black) #Texto
    gameDisplay.blit(text, (350, 250)) #Renderizado

    # Final Score
    font = pygame.font.SysFont(None, 115) #Tamaño de Fuente
    text = font.render("Score : " + str(score), True, black) #Texto
    gameDisplay.blit(text, (165, 170)) #Renderizado


# This function print obstacle cars
def draw_things(thingx, thingy, thing):
    gameDisplay.blit(thing, (thingx, thingy)) #Dibujamos los autos obstaculos en la via


# This function print our car
def car(x, y):
    gameDisplay.blit(carImg, (x, y)) #Dibujamos el auto del usuario


# this function make the rectangles for buttons from initial menu
def text_objects(text, font):#Botones dle menu
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


# This functio print buttons
def message_display(text, size, x, y): #Esta funcion se utiliza para la mayoria de mensajes que muestra el juego
    font = pygame.font.Font("./assets/CaviarDreams.ttf", size)#Fuente
    text_surface, text_rectangle = text_objects(text, font) #Texto
    text_rectangle.center = (x, y) #Bloque
    gameDisplay.blit(text_surface, text_rectangle) #render

def crash(x,y,score): #Funcion de choque
    pygame.mixer.Sound.play(crash_sound) #Sonido de choque
    pygame.mixer.music.stop()#Detenemos toda la musica
    reset = 3 #contador
    #Stop Music
    #this put the crach img in the cash car position
    gameDisplay.blit(crash_img,(x,y)) #Imagen de choque
    # Put Message, update display, and wait
    message_display("You Crashed",115,display_width/2,display_height/2) #Mensaje de choque
    pygame.display.update() #Actualizar vista
    time.sleep(3)#Esperar

    while reset >= 0: #Ciclo para el contador despues de chocar
        gameDisplay.fill(white)#fondo blanco
        try_again_counter(reset,score) #Dipslay counter
        pygame.display.update()
        time.sleep(1)
        reset-=1
    time.sleep(0.5)
    intro()#Abrir el menu de inicio
    gameloop() #Reiniciar variables del juego

#Funcion para el juego
def gameloop():
    global car_x_change #Variable de cambio para el auto
    pygame.mixer.Sound.play(start_sound) #Sonido de inicio
    pygame.mixer.music.stop()
    pygame.mixer.music.load("./assets/game.mp3")#Musica de fondo
    pygame.mixer.music.play(-1)#Musica de fondo
    #Variables de inicio para el fondo
    bg_x1 = 0
    bg_x2 = 0
    bg_y1 = 0
    bg_y2 = -600
    bg_speed = 6 #Velocidad inicial del fondo
    bg_speed_change = 0 #Velocidad de cambio
    car_x = ((display_width / 2) - (car_width / 2)) #Posición del auto
    car_y = (display_height - car_height) #Posición del auto
    car_x_change = 0 #Velocidad de cambio de los obstaculos
    road_start_x = (display_width / 2) - 112 #Posición de la carretera
    road_end_x = (display_width / 2) + 112 #Posición de la carretera

    thing_startx = random.randrange(road_start_x, road_end_x - car_width) #Auto obstaculo random 
    thing_starty = -600 #Posición inicial del obstaculo
    #variables del estado del juego
    thingw = 50
    thingh = 100
    thing_speed = 1 #obstaculos
    count = 0 #Score
    pause = False #pausa
    gameExit = False #ejecutando

    while not gameExit: #Ciclo de juego

        for event in pygame.event.get(): #Listene de eventos

            if event.type == pygame.QUIT: #Opcion para cerrarlo
                gameExit = True
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: #alternativas de control
                # Here we can put the camera results
                if event.key == pygame.K_LEFT: #Movimiento a la izquierda
                    car_x_change = -1.5
                elif event.key == pygame.K_RIGHT: #Movimiento a la derecha
                    car_x_change = 1.5
                elif event.key == pygame.K_SPACE: #Pausa
                    pause = True

            if event.type == pygame.KEYUP: #Detenerse
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    car_x_change = 0

        while pause == True: #Ciclo de pausa
            pygame.mixer.music.pause() #pausar la musica
            message_display("Game Paused",115,display_width/2,display_height/2) #Mostrar mensaje
            pygame.display.update()
            time.sleep(0.5) #Esperar
            gameDisplay.blit(bgImg, (bg_x1, bg_y1)) #Objetos estaticos
            gameDisplay.blit(bgImg2, (bg_x2, bg_y2))#Objetos estaticos
            car(car_x, car_y)  #Objetos estaticos
            draw_things(thing_startx, thing_starty, car2Img) #Objetos estaticos
            highscore(count) #Objetos estaticos
            pygame.display.update() #Actualiza objetos
            time.sleep(0.5) #esperar
            for event in pygame.event.get(): #Si se presiona space reanuda
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Continue...")
                        pygame.mixer.music.unpause() #reanudar sonido
                        pause = False #Quitar pausa
                        

        car_x += car_x_change

        if car_x > road_end_x - car_width: #choque borde de la carretera
            crash(car_x, car_y, count)
        if car_x < road_start_x: #choque borde de la carretera
            crash(car_x - car_width, car_y, count)

        if car_y < thing_starty + thingh - 25: #choque de frente
            if car_x >= thing_startx + 10 and car_x <= thing_startx + thingw - 10: #choque de izquierdo con obstaculo
                # Left Crash
                crash(car_x - car_width /2, car_y - car_height / 2, count)
            if car_x + car_width >= thing_startx + 13 and car_x + car_width <= thing_startx + thingw + 10: #choque en la derecha con obstaculo
                # Right Crash
                crash(car_x, car_y - car_height / 2, count)

        gameDisplay.blit(bgImg, (bg_x1, bg_y1)) #Actualización Renderizado de fondo1
        gameDisplay.blit(bgImg2, (bg_x2, bg_y2)) #Actualización Renderizado de fondo2

        car(car_x, car_y)  #Actualización Auto
        draw_things(thing_startx, thing_starty, car2Img) #Actualización Renderizado de osbtaculo
        highscore(count) #Actualización del score
        count += 1 #Aumenta el score

        # Update Speed Obstacle Cars
        thing_speed += 0.001
        thing_starty += thing_speed

        if thing_starty > display_height: #Actualización de autos obstaculo
            thing_startx = random.randrange(road_start_x, road_end_x - car_width)
            thing_starty = -200

        bg_y1 += bg_speed
        bg_y2 += bg_speed

        if bg_y1 >= display_height: #Actualización de fondo1
            bg_y1 = -600

        if bg_y2 >= display_height: #Actualización de fondo2
            bg_y2 = -600
        #camera()
        pygame.display.update()  # update the screen
        clock.tick(128)  # frame per sec

#-----------------------------------------------------------------------------------------------------------
# . HILOS
#-----------------------------------------------------------------------------------------------------------
#Debido a que la camara debe funcionar de manera independiente se creo un hilo para tal fin usando la librería mencionada anteriormente
threadCamera = threading.Thread(target=openCamera)
threadCamera.start()

