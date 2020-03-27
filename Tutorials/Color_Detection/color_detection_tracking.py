"""
Color_Detection_Tracking
Se va a detectar colores, realizar el borde o contornos e incontrar las coordenas del centro de la imagen a detectar (azul
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# Definimos los rango a detectar con base en la siguiente tabla
# https://i.stack.imgur.com/gyuw4.png
azulBajo = np.array([100,100,20])
azulAlto = np.array([125,255,255])

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,1)
    if ret == True:
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #Aplicamos la mascara
        mask = cv2.inRange(frameHSV,azulBajo,azulAlto)
        #Obtenemos los contornos de las partes blancas y los dibujamos
        contornos,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        """
        Dibujamos todos los contornos, con 
        -1 indicamos que dibuje todos los encontrados
        (255,0,0) indica que va dibujar los contornos azules BGR
        3 indica el grosor de la linea a dibujar.
        """
        #cv2.drawContours(frame, contornos, -1, (255,0,0),3)
        #Como se dibujan multiples contornos, solo seleccionaremos los que cumplan cierta area.
        for contor in contornos:
            area = cv2.contourArea(contor)
            if area > 3000:
                #Buscamos las coordenadas del centro
                centros = cv2.moments(contor)
                if(centros["m00"]==0):centros["m00"]=1
                x =int(centros["m10"]/centros["m00"])
                y = int(centros["m01"]/centros["m00"])
                # 7 indica el radio
                cv2.circle(frame,(x,y),7,(0,255,0),-1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,'{},{}'.format(x,y),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
                # Luego de eliminar los contorno menores a cierta area, vamos a suavizar los contornos
                contorSuavi = cv2.convexHull(contor)
                cv2.drawContours(frame,[contorSuavi],0,(255,0,0),3)
        #cv2.imshow('MaskAzul',mask)




        cv2.imshow('Original',frame)


        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
cap.release()
cv2.destroyAllWindows()