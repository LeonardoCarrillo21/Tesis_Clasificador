import cv2
import csv
import numpy as np

class Base:

    def __init__(self,nombreArchivo='test.csv',puntos=50):
        self.nombreArchivo = nombreArchivo
        self.orb = cv2.ORB_create()
        self.escritor = csv.writer(open(nombreArchivo,mode="a",newline=''))
        self.lector = None
        self.puntos=puntos

    def guardar(self,img,etiqueta='botella'):
        print("guardando fila")
        _,detectores = self.orb.detectAndCompute(img,None)
        renglon = [valor for detector in detectores[:self.puntos] for valor in detector]
        renglon.append(etiqueta)
        self.escritor.writerow(renglon)

    def cargarBase(self):
        print("leyendo csv")
        self.lector = csv.reader(open(self.nombreArchivo,'r'))
        base = np.array([np.array([int(dato) for dato in fila[:-1]]).reshape(self.puntos,32) for fila in self.lector])
        return base

    def ejemplo(self):
        path = "botellas descargadas/5.jpg"
        imagen = cv2.imread(path,0)
        # self.guardar(imagen)
        base = self.cargarBase()
# Base().ejemplo()

