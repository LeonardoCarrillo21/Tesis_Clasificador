import cv2
import numpy as np

class Momentos:
    def __init__ (self):
        pass

    def getMomentos(self,imagen):

        momentos = cv2.moments(imagen)
        momenhu = cv2.HuMoments(momentos) #vector de 7 x 1  reglones de un elemento
        vect = np.reshape(momenhu,(1,7)) #vector de 1 x 7  convertido
        vect = vect[0][:3]
        # print("momentos hu ", vect[0]) # imprimir el vector
        return vect

# imagen = cv2.imread("1.jpg",0)
# obj = Momentos()
# obj.getMomentos(imagen)
