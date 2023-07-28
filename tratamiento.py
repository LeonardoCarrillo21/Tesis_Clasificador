import csv
import cv2
import numpy as np
from momentos import Momentos
import matplotlib.pyplot as plt


class Tratamiento:

    def __init__(self,
                 path='botellas/1.jpg',
                 algoritmo_bordes="canny",
                 repite_suavisado=3,
                 binariza=True,
                 carpeta="Enontrados",
                 clase="botella"):
        self.path = path
        self.repite_suavisado = repite_suavisado
        self.binariza = binariza
        self.algoritmo_bordes = algoritmo_bordes
        self.carpeta=carpeta
        self.clase=clase
        self.nombreArchivo = "baseMomentos.csv"
        self.escritor = csv.writer(open(self.nombreArchivo,mode="a",newline=''))
        self.lector = None
        self.mom = Momentos()
        self.areaMinima = 500

    def suave(self,image):
        #se suavisa
        for i in range(self.repite_suavisado):
            image = cv2.GaussianBlur(image, (5, 5), 0)
        return image


    def guardarMomentos(self,img,etiqueta):
        momentos = cv2.moments(img)
        momenhu = cv2.HuMoments(momentos) #vector de 7 x 1  reglones de un elemento
        vect = np.reshape(momenhu,(1,7)) #vector de 1 x 7  convertido
        vect = vect[0][:3]
        vect = np.concatenate((vect,[etiqueta]))
        self.escritor.writerow(vect)


    def encontrarAreas2(self,imagen):
        contornos, jerarquia = cv2.findContours(imagen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        baseNegra=np.zeros_like(imagen)

        contornos_encontrados=[cnt for cnt in contornos if cv2.contourArea(cnt)>100]
        for contorno in contornos_encontrados:
            epsilon = 0.01 * cv2.arcLength(contorno, True)
            aprox_poligonal = cv2.approxPolyDP(contorno, epsilon, True)
            # Dibujar el contorno cerrado
            
            cv2.drawContours(baseNegra, [aprox_poligonal], 0, (0, 255, 0), 2)    
        plt.imshow(cv2.cvtColor(baseNegra,cv2.COLOR_GRAY2RGB))
        plt.axis('off')
        plt.show()

    def encontrarAreas(self,imagen):
        contornos,_=cv2.findContours(imagen,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        print(f'contornos totales: {len(contornos)}')
        contornos_encontrados=[cnt for cnt in contornos if cv2.contourArea(cnt)>self.areaMinima]
        baseNegra=np.zeros_like(imagen)
        print(f'contornos resultantes: {len(contornos_encontrados)}')
        cv2.drawContours(baseNegra,contornos_encontrados,-1,(255),thickness=cv2.FILLED)
        
        self.mostrarYEsperar([f"Areas > {self.areaMinima}"],[baseNegra])

    def sobel(self,image):

        # Aplicar el operador de Sobel en las direcciones horizontal y vertical
        gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

        # Calcular la magnitud y la dirección del gradiente
        gradient_magnitude = cv2.magnitude(gradient_x, gradient_y)
        gradient_angle = cv2.phase(gradient_x, gradient_y, angleInDegrees=True)
    
        # Mostrar las imágenes resultantes
        self.mostrarYEsperar(['original','Gradient X','Gradient Y','Gradient Magnitude','Gradient Angle'],[image,gradient_x,gradient_y,gradient_magnitude,gradient_angle])
        return (gradient_magnitude  * 255).astype(np.uint8)

    def mostrarPLT(self,nombre,imagen):
        plt.imshow(nombre,cv2.cvtColor(imagen,cv2.COLOR_GRAY2RGB))
        plt.axis("off")
        plt.show()
    def mostrarYEsperar(self,nombres,imagenes):
        for nombre,imagen in zip(nombres,imagenes):
            cv2.imshow(nombre,imagen)
            cv2.waitKey(0)

    def tratamiento(self):
        im = cv2.imread(self.path,0)
        im = cv2.resize(im,(400,400))

        # suave = self.suave(im)
        # self.mostrarYEsperar([f"suave {self.repite_suavisado} veces"],[suave])
        self.mostrarYEsperar([f"original"],[im])

        if self.binariza:
            _, imagen_binaria = cv2.threshold(im,0, 255, cv2.THRESH_OTSU)
            cv2.imshow(f"binarizada",imagen_binaria)
            cv2.waitKey()
            cv2.destroyAllWindows()
        else:
            imagen_binaria = im


        ##cierre 
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        cierre = cv2.morphologyEx(imagen_binaria,cv2.MORPH_CLOSE,kernel)
        

        ##apertura
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        apertura = cv2.morphologyEx(cierre,cv2.MORPH_OPEN,kernel)
        
        self.mostrarYEsperar(["cierre","apertura"],[cierre,apertura])

        if self.algoritmo_bordes=="canny":
            bordes = cv2.Canny(apertura,100,300)
            self.mostrarPLT("canny",bordes)
        if self.algoritmo_bordes=="sobel":
            bordes = self.sobel(apertura)

        self.encontrarAreas(bordes)
        # self.guardarMomentos(bordes,self.clase)
        return bordes