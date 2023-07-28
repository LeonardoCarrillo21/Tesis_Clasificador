import cv2
import numpy as np

class ORB:

    def __init__(self):
        # Crear objeto ORB
        self.orb = cv2.ORB_create()

    def detectarCompatibilidad(self,image1, image2):
        '''
        Descripcion de la funcion.
        funcion que detecta puntos de interes en 2 imagenes y detecta la compatibilidad entre ambas
        
        '''
        keypoints1, descriptors1 = self.orb.detectAndCompute(image1, None)
        keypoints2, descriptors2 = self.orb.detectAndCompute(image2, None)
        print(descriptors1)
        print(len(descriptors1))
        # Realizar emparejamiento de características
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        matches = sorted(matches, key=lambda x: x.distance)
        print(len(matches))
        # Dibujar emparejamientos en una nueva imagen
        matched_image = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:30], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('Matches', matched_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def ejemplo(self):
        image1 = cv2.imread('Entrenamiento/botella/plastic3.jpg', cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread('botellas descargadas/5.jpg', cv2.IMREAD_GRAYSCALE)
        # suave1 = cv2.GaussianBlur(image1, (5, 5), 0)
        # bordes1=cv2.Canny(suave1,100,300) 
        # suave2 = cv2.GaussianBlur(image2, (5, 5), 0)
        # bordes2=cv2.Canny(suave2,100,300)
        self.detectarCompatibilidad(image1.copy(),image2.copy())
ORB().ejemplo()