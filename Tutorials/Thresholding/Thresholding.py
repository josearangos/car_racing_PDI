"""
Umbralización o Thresholding

Método de segmentación más básico, que lo que busca es separar el fonde de la imagen del objeto de interes
Se suele usar imagenes donde el objeto de interes es diferenciable del fondo

Necesitamos de:
- Imagen en escala de grises
- Umbral entre 0-255
"""
import cv2
import numpy as np
import imutils  #usada para redimensionar una imagen
#path ='balon.jpg'
path = 'perfil'
#Leemos la imagen
img = cv2.imread(path,0) #usando cero la leemos en escala de grises
img = imutils.resize(img,width=400)

#Tipos de umbralización
# parametros imagen, umbral, valor y tipo de umbralización

#Tipos de umbralización BINARY
# los pixles con valores mayores al umbral se colocaran en blanco(255) y los demos en negro
_,binarizada = cv2.threshold(img,90,255,cv2.THRESH_BINARY)
_,binarizadaInv = cv2.threshold(img,90,255,cv2.THRESH_BINARY_INV)

#Tipo de umbralización TRUNCATE
# si el valor del pixel supera el umbral se toma los valores del umbral
_,trun = cv2.threshold(img,90,255,cv2.THRESH_TRUNC)

#Tipo de umbralización To Zero- To zero inveritido
#Si el valor del pixel supera el umbral, se mantiene el valor de la imagen original
_,ToZ = cv2.threshold(img,90,255,cv2.THRESH_TOZERO)
_,ToZInv = cv2.threshold(img,90,255,cv2.THRESH_TOZERO_INV)



cv2.imshow('Imagen: Original - Binary - Binary Invertido - Truncate  -  ToZero -  ToZInv',np.hstack([img,binarizada,binarizadaInv,trun,ToZ,ToZInv]))

cv2.waitKey(0)
cv2.destroyAllWindows()