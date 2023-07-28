import cv2
import os
import numpy as np

def apertura(imagen):
    kernel = np.ones((3, 3), np.uint8)  # Puedes ajustar el tamaño del kernel según tus necesidades
    # Aplicar la apertura
    opened_image = cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)
    return opened_image
def mostrarYEsperar(nombres,imagenes):
    for nombre,imagen in zip(nombres,imagenes):
        cv2.imshow(nombre,imagen)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
def suave(image,veces):
        #se suavisa
        for i in range(veces):
            image = cv2.GaussianBlur(image, (5, 5), 0)
        return image
def leer(path,nombres):
    return [cv2.imread(path+'/'+nombre,0) for nombre in nombres]

def buscar(path):
    return os.listdir(path)
def binarizar(imagenes):
    return [ cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)[1] for imagen in imagenes]

def redimensionar(imagenes,N,M):
    return [cv2.resize(imagen,(N,M)) for imagen in imagenes]

def principal():
    path = "botellas descargadas"
    nombres = buscar(path)
    originales = leer(path,nombres)
    redimensionadas = redimensionar(originales,400,400)
    
    binarias = binarizar(redimensionadas)
    mostrarYEsperar(nombres,binarias)
    suavisadas = [suave(imagen,1) for imagen in originales]
    binarias_suavisadas = binarizar(suavisadas)
    cannys = [cv2.Canny(imagen,100,300) for imagen in binarias_suavisadas]
    # aperturadas = [apertura(imagen) for imagen in cannys]

    

principal()