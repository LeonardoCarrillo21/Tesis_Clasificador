import os
from momentos import Momentos
import cv2
import csv
import numpy as np

class GeneradorBaseDescriptores:

    def __init__(self,nombreArchivo='baseMomentos.csv',puntos=2):
        self.nombreArchivo = nombreArchivo
        self.orb = cv2.ORB_create()
        self.escritor = csv.writer(open(nombreArchivo,mode="a",newline=''))
        self.lector = None
        self.puntos=puntos
        self.mom = Momentos()
    
    def guardar(self,img,etiqueta='botella'):
        print("guardando fila")
        # a cada imagen le obtiene los puntos y el vector de cada punto
        _,detectores = self.orb.detectAndCompute(img,None)
        if detectores is not None and len(detectores)>=self.puntos:
            renglon = [valor for detector in detectores[:self.puntos] for valor in detector] #pega los vectores en 1 linea
            renglon.append(etiqueta) #agrega la etiqueta
            self.escritor.writerow(renglon) #AGREGA A LA BASE

    def guardarMomentos(self,img,etiqueta='botella'):
        momentos = cv2.moments(img)
        momenhu = cv2.HuMoments(momentos) #vector de 7 x 1  reglones de un elemento
        vect = np.reshape(momenhu,(1,7)) #vector de 1 x 7  convertido
        vect = vect[0][:3]
        vect = np.concatenate((vect,[etiqueta]))
        self.escritor.writerow(vect)
    
    def getMomentos(self,img):
        momentos = cv2.moments(img)
        momenhu = cv2.HuMoments(momentos) #vector de 7 x 1  reglones de un elemento
        vect = np.reshape(momenhu,(1,7)) #vector de 1 x 7  convertido
        vect = vect[0][:3]
        return vect

    def tratamiento(self,im):
        suave = cv2.GaussianBlur(im, (5, 5), 0)
        _, imagen_binaria = cv2.threshold(suave, 127, 255, cv2.THRESH_BINARY)
        bordes = cv2.Canny(imagen_binaria,100,300)
        return bordes
    def buscar(self,ruta,etiqueta):
        for nombre in os.listdir(ruta): # [archivo,archivo,carpeta]            
            ruta_com = os.path.join(ruta,nombre) # C:\Users\atrej\Desktop\10 semestre\Tratamiento de imagens (R)\PROYECTO\Training + [archivo]
            esDirectorio = os.path.isdir(ruta_com)
            if esDirectorio:
                self.buscar(ruta_com,nombre)
            if not os.path.isdir(ruta_com):
                # print(ruta_com)
                imagenleida = cv2.resize(cv2.imread(ruta_com,0),(400,400))
                # self.guardar(imagenleida,etiqueta)
                tratada=self.tratamiento(imagenleida)
                self.guardarMomentos(tratada,etiqueta)

# ruta = os.getcwd()+"\Entrenamiento"
# print("buscando en : ",ruta)
# obj1= GeneradorBaseDescriptores("baseDetectores.csv",50)
# obj1.buscar(ruta,"")