import os
from momentos import Momentos
import cv2
import csv
import numpy as np
# from gauss import Gauss
# from Apertura import Apertura1

class Generador:

    def __init__ (self):# la primera fucnion que se va llamar al crear un objeto de la clase generador
        self.momentos = Momentos()  #variable que conoce toda la clase

    def buscar(self,ruta,etiqueta):
        lineas=[]
        '''
        [
            [momentos+etiqueta]
            [momentos+etiqueta]
            [momentos+etiqueta]
            [momentos+etiqueta]
        ]

        '''
        # contador=0
        for nombre in os.listdir(ruta): # [archivo,archivo,carpeta]
            ruta_com = os.path.join(ruta,nombre) # C:\Users\atrej\Desktop\10 semestre\Tratamiento de imagens (R)\PROYECTO\Training + [archivo]
            esDirectorio = os.path.isdir(ruta_com)
            if esDirectorio:
                print("carpeta :",nombre)
                self.buscar(ruta_com,nombre)

            if not esDirectorio:
                mom = self.momentos.getMomentos(cv2.Canny(cv2.resize(cv2.imread(ruta_com,0),(100,100)),100,300))     
                mom = mom.tolist()
                mom = mom[:3]
                print("momentos hu ",mom) # imprimir el vector
                mom.extend([etiqueta])
                lineas.append(mom)

        csv.writer(open('Base.csv',mode='a',newline='')).writerows(lineas)

# ruta = os.getcwd()+"\Training"
# print("buscando en : ",ruta)

# obj1= Generador()
# obj1.buscar(ruta," ")
