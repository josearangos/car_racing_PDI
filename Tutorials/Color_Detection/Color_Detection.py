""""
Color_Detection
Existen diversos espacios de colores:

- Modelo cordenadas formato RGB
- Modelo cordenadas HSV
- Modelo cordenadas LAB o CIE

Usaremos el espacio de color HSV
-H: Hue/Matiz
-S: Saturation/Saturación
-V: Value/Brillo

En OpenCV: el rango de valores que puede toma
- H: 0 a 179
- S: 0 a 255
- V: 0 a 255

Pasos
1. Leemos la imagen o capturamos los frames del video
2. Transformar de BGR a HSV
3. Definir rangos del color a detectar
4. Crear las mascaras con los rangos de colores.
5. visualización de la detección de los colores
"""
import cv2
import numpy as  np

cap =cv2.VideoCapture(0)

#Para este ejemplo vamos a detectar el color rojo por lo tanto definimos los rangos de este
# En el siguiente enlace podras encontrar  la escala cromatica del espacio de color HSV
# https://i.stack.imgur.com/gyuw4.png
redBajo1=np.array([0,100,20])
redAlto1=np.array([8,255,255])
redBajo2=np.array([175,100,20])
redAlto2=np.array([179,255,255])

while True:
    ret,frame = cap.read()
    if ret == True:
        # Usamos flip 1 para girar el frame horizontalmente
        frame = cv2.flip(frame,1)
        #Transformar de BGR a HSV
        frameHSV =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #Crear las mascaras de colores a detectara
        maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
        maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
        maskRed = cv2.add(maskRed1,maskRed2)
        # las partes blancas son aquellas que caen en el rango definido, mientras las negras son las que no
        cv2.imshow('Mascara Roja', maskRed)
        #Mostraremos el color original, para eso usamos la función bitWise
        maskRedBitWise = cv2.bitwise_and(frame,frame,mask=maskRed)
        cv2.imshow('Mascara Roja -Color original', maskRedBitWise)

        #cv2.imshow('Frame',np.hstack([frame,frameHSV]))
        ##Presionando la tecla 'S' salimos
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
cap.release()
cv2.destroyAllWindows()


