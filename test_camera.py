import cv2
import numpy as  np

cap =cv2.VideoCapture(2)
cordeX, cordeY = 0,0
val = 0
font = cv2.FONT_HERSHEY_SIMPLEX
def pointCoordenates(frame):
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

while(cap.isOpened()):
    ret,frame = cap.read()
    frame =cv2.flip(frame,1)
    if ret==True:
        fil=frame.shape[0]
        col = frame.shape[1]
        x_medio_derecha=int((col+60)/2)
        x_medio_izquierda =int((col-60)/2)

        cordeX =  int(col/2)
        cordeY = int(fil/2)

        #Linea derecha
        cv2.line(frame,(x_medio_derecha,0),(x_medio_derecha,fil),(0,255,0),2)
        #Linea izquierda
        cv2.line(frame, (x_medio_izquierda, 0), (x_medio_izquierda, fil), (0, 255, 0), 2)
        pointCoordenates(frame)

        #izquierda
        if(cordeX>0 and  cordeX<x_medio_izquierda):
            val = -1.5
        if(cordeX>=x_medio_izquierda and cordeX<=x_medio_derecha):
            val = 0
        if(cordeX>x_medio_derecha and cordeX<col):
            val = 1.5

        cv2.putText(frame,str(val),(20,20),font, 0.75,(0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame,'CordX: '+ str(cordeX), (20, 60), font, 0.75, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
cap.release()
cv2.destroyAllWindows()









"""
def insertCamera():
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Usamos flip 1 para girar el frame horizontalmente
            # Transformar de BGR a HSV
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frameRGB = cv2.resize(frameRGB, (440, 280))
            gameDisplay.fill([0, 0, 0])  # Fills the screen with black
            frameRGB = np.rot90(frameRGB)
            frameRGB = pygame.surfarray.make_surface(frameRGB)
            gameDisplay.blit(frameRGB, (440, 320))
            pygame.display.update()  # This updates the screen so we can see our rectangle
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)


"""