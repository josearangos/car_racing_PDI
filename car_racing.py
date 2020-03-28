import cv2
import numpy as  np
import pygame
import time
import random


class CAR_GAME():

    def __init__(self):
            cordeX, cordeY = 0,0
            pygame.init()
            self.display_width = 800
            self.display_height = 600

            self.black = (0, 0, 0)
            self.white = (255, 255, 255)
            self.green = (0, 255, 0)
            self.red = (255, 0, 0)
            self.blue = (0, 0, 255)

            self.car_width = 50
            self.car_height = 100
            # pygame.mixer.music.load("assets/Hurry_Up.mp3")
            self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
            pygame.display.set_caption("Car Racing")
            self.clock = pygame.time.Clock()

            ##Cargar en otro momento
            self.carImg = pygame.image.load("assets/car3.png")  # load the car image
            self.car2Img = pygame.image.load("assets/car2.png")
            self.bgImg = pygame.image.load("assets/back2.jpg")
            self.bgImg2 = pygame.image.load("assets/back3.jpg")
            self.crash_img = pygame.image.load("assets/crash.png")
            self.cap =cv2.VideoCapture(2) # Es la camara del celular
            car_x_change = 0
            self.font = cv2.FONT_HERSHEY_SIMPLEX

    def pointCoordenates(self,frame):
        global cordeX, cordeY
        azulBajo = np.array([100, 100, 20])
        azulAlto = np.array([125, 255, 255])
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Aplicamos la mascara
        mask = cv2.inRange(frameHSV, azulBajo, azulAlto)
        # Obtenemos los contornos de las partes blancas y los dibujamos
        contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        """
        Dibujamos todos los contornos, con 
        -1 indicamos que dibuje todos los encontrados
        (255,0,0) indica que va dibujar los contornos azules BGR
        3 indica el grosor de la linea a dibujar.
        """
        # cv2.drawContours(frame, contornos, -1, (255,0,0),3)
        # Como se dibujan multiples contornos, solo seleccionaremos los que cumplan cierta area.
        for contor in contornos:
            area = cv2.contourArea(contor)
            if area > 700:
                # Buscamos las coordenadas del centro
                centros = cv2.moments(contor)
                if (centros["m00"] == 0): centros["m00"] = 1
                x = int(centros["m10"] / centros["m00"])
                y = int(centros["m01"] / centros["m00"])
                cordeX = x
                cordeY = y
                # 7 indica el radio
                cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
                # Luego de eliminar los contorno menores a cierta area, vamos a suavizar los contornos
                contorSuavi = cv2.convexHull(contor)
                cv2.drawContours(frame, [contorSuavi], 0, (255, 0, 0), 3)

    def openCamera(self):
        global car_x_change,cordeX,cordeY
        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            if ret == True:
                fil = frame.shape[0]
                col = frame.shape[1]
                x_medio_derecha = int((col + 60) / 2)
                x_medio_izquierda = int((col - 60) / 2)
                cordeX = int(col / 2)
                cordeY = int(fil / 2)
                # Linea derecha
                cv2.line(frame, (x_medio_derecha, 0), (x_medio_derecha, fil), (0, 255, 0), 2)
                # Linea izquierda
                cv2.line(frame, (x_medio_izquierda, 0), (x_medio_izquierda, fil), (0, 255, 0), 2)
                self.pointCoordenates(frame)
                # izquierda
                if (cordeX > 0 and cordeX < x_medio_izquierda):
                    car_x_change = -0.5
                if (cordeX >= x_medio_izquierda and cordeX <= x_medio_derecha):
                    car_x_change = 0
                if (cordeX > x_medio_derecha and cordeX < col):
                    car_x_change = 0.5
                cv2.putText(frame, str(car_x_change), (20, 20), self.font, 0.75, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'CordX: ' + str(cordeX), (20, 60), self.font, 0.75, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break
        self.cap.release()
        cv2.destroyAllWindows()

    def intro(self):
        # pygame.mixr.Sound.play(start_music)
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
            pygame.display.set_icon(self.carImg)

            pygame.draw.rect(self.gameDisplay, self.black, (200, 400, 100, 50))
            pygame.draw.rect(self.gameDisplay, self.black, (500, 400, 100, 50))

            self.gameDisplay.fill(self.white)
            self.message_display("CAR RACING", 100, self.display_width / 2, self.display_height / 2)
            self.gameDisplay.blit(self.carImg, ((self.display_width / 2) - 100, 10))
            pygame.draw.rect(self.gameDisplay, self.green, (200, 400, 100, 50))
            pygame.draw.rect(self.gameDisplay, self.red, (500, 400, 100, 50))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if menu1_x < mouse[0] < menu1_x + menu_width and menu1_y < mouse[1] < menu1_y + menu_height:
                pygame.draw.rect(self.gameDisplay, self.blue, (200, 400, 100, 50))
                if click[0] == 1:
                    intro = False
            if menu2_x < mouse[0] < menu2_x + menu_width and menu2_y < mouse[1] < menu2_y + menu_height:
                pygame.draw.rect(self.gameDisplay, self.blue, (500, 400, 100, 50))
                if click[0] == 1:
                    pygame.quit()
                    quit()

            self.message_display("Go", 40, menu1_x + menu_width / 2, menu1_y + menu_height / 2)
            self.message_display("Exit", 40, menu2_x + menu_width / 2, menu2_y + menu_height / 2)
            pygame.display.update()
            self.clock.tick(50)

    # This function update the score
    def highscore(self,count):
        font = pygame.font.SysFont(None, 60)
        text = font.render("Score : " + str(count), True, self.black)
        self.gameDisplay.blit(text, (0, 0))

    def try_again_counter(self,count, score):
        # Try Again Timer
        font = pygame.font.SysFont(None, 250)
        text = font.render(str(count), True, self.black)
        self.gameDisplay.blit(text, (350, 250))

        # Final Score
        font = pygame.font.SysFont(None, 115)
        text = font.render("Score : " + str(score), True, self.black)
        self.gameDisplay.blit(text, (165, 170))


    # This function print obstacle cars
    def draw_things(self,thingx, thingy, thing):
        self.gameDisplay.blit(thing, (thingx, thingy))


    # This function print our car
    def car(self,x, y):
        self.gameDisplay.blit(self.carImg, (x, y))


    # this function make the rectangles for buttons from initial menu
    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()


    # This functio print buttons
    def message_display(self, text, size, x, y):
        font = pygame.font.Font("assets/CaviarDreams.ttf", size)
        text_surface, text_rectangle = self.text_objects(text, font)
        text_rectangle.center = (x, y)
        self.gameDisplay.blit(text_surface, text_rectangle)

    def crash(self, x,y,score):
        reset = 3
        #Stop Music
        pygame.mixer.music.stop()

        #this put the crach img in the cash car position
        self.gameDisplay.blit(self.crash_img,(x,y))

        #Put Message, update display, and wait
        self.message_display("You Crashed",115,self.display_width/2,self.display_height/2)
        pygame.display.update()
        time.sleep(3)

        while reset > -1:
            self.gameDisplay.fill(self.white)
            self.try_again_counter(reset,score)
            time.sleep(1)
            reset-=1
            pygame.display.update()
        self.intro()
        self.gameloop() #for restart the game

    def gameloop(self):
        global car_x_change
        # pygame.mixer.Sound.stop()
        # pygame.mixer.music.play(-1)
        bg_x1 = 0
        bg_x2 = 0
        bg_y1 = 0
        bg_y2 = -600
        bg_speed = 6
        bg_speed_change = 0
        car_x = ((self.display_width / 2) - (self.car_width / 2))
        car_y = (self.display_height - self.car_height)
        car_x_change = 0
        road_start_x = (self.display_width / 2) - 112
        road_end_x = (self.display_width / 2) + 112

        thing_startx = random.randrange(road_start_x, road_end_x - self.car_width)
        thing_starty = -600
        thingw = 50
        thingh = 100
        thing_speed = 1
        count = 0
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

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        car_x_change = 0

            car_x += car_x_change

            if car_x > road_end_x - self.car_width:
                self.crash(car_x, car_y, count)
            if car_x < road_start_x:
                self.crash(car_x - self.car_width, car_y, count)

            if car_y < thing_starty + thingh - 25:
                if car_x >= thing_startx + 10 and car_x <= thing_startx + thingw - 10:
                    # Left Crash
                    self.crash(car_x - 25, car_y - self.car_height / 2, count)
                if car_x + self.car_width >= thing_startx - 10 and car_x + self.car_width <= thing_startx + thingw + 10:
                    # Right Crash
                    self.crash(car_x, car_y - self.car_height / 2, count)

            self.gameDisplay.blit(self.bgImg, (bg_x1, bg_y1))
            self.gameDisplay.blit(self.bgImg2, (bg_x2, bg_y2))

            self.car(car_x, car_y)  # display car
            self.draw_things(thing_startx, thing_starty, self.car2Img)
            self.highscore(count)
            count += 1

            # Update Speed Obstacle Cars
            thing_speed += 0.000
            thing_starty += thing_speed

            if thing_starty > self.display_height:
                thing_startx = random.randrange(road_start_x, road_end_x - self.car_width)
                thing_starty = -200

            bg_y1 += bg_speed
            bg_y2 += bg_speed

            if bg_y1 >= self.display_height:
                bg_y1 = -600

            if bg_y2 >= self.display_height:
                bg_y2 = -600

            pygame.display.update()  # update the screen
            self.clock.tick(128)  # frame per sec



