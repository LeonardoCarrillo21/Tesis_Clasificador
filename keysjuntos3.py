import cv2
import numpy as np
import os
class Keys:
    def __init__(self,
                 path='botellas/1.jpg',
                 cany=True,
                 repite_suavisado=3,
                 puntos=50,
                 binariza=True,
                 carpeta="Enontrados",
                 clase="botella"):
        self.path = path
        self.repite_suavisado = repite_suavisado
        self.puntos = puntos
        self.binariza = binariza
        self.cany = cany
        self.carpeta=carpeta
        self.clase=clase

    def suave(self,image):
        #se suavisa
        for i in range(self.repite_suavisado):
            image = cv2.GaussianBlur(image, (5, 5), 0)
        return image

    def keys(self):
        #leer imagen
        image = cv2.imread(self.path, cv2.IMREAD_COLOR)    
        # redimensionar (400,400)
        image = cv2.resize(image,(400,400))
        
        if self.binariza:
            gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, imagen_binaria = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
            imagen_binaria = self.suave(imagen_binaria)
            cv2.imshow("binaria",imagen_binaria)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            #suavisar N veces
            image = self.suave(image)
            #base Obscura
        
        negra = np.zeros_like(image)
        # Crear el objeto detector
        detector = cv2.ORB_create()
        #bordes
        
        if self.cany:
            if self.binariza:
                bordes = cv2.Canny(imagen_binaria,100,300)
            else:
                bordes = cv2.Canny(image,100,300)
            # Detectar puntos clave
            keypoints,detectors = detector.detectAndCompute(bordes, None)

        else:
            keypoints,detectors = detector.detectAndCompute(image, None)

        #keypoints ordenados segun el atributo response
        keypoints_ordenado = sorted(keypoints, key=lambda kp: kp.response, reverse=True)

        #reduciendo cantidad de keypuntos a self.puntos
        print(f"hay {len(keypoints)} puntos de interes en la imagen")
        keypoints=keypoints[:self.puntos]
        
        ##########################################
        # Dibujar y mostrar los puntos clave en la imagen
        ##########################################        
        #dibujando keys rojos
        negra_con_keypoints = cv2.drawKeypoints(negra, keypoints[:self.puntos], None, color=(0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)        
        #imagen con puntos N rojos interes
        suave_con_keypoints = cv2.drawKeypoints(image, keypoints[:self.puntos], None, color=(0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #Mostrar la imagen con los puntos clave
        cv2.imshow(f'original {self.repite_suavisado} suavisados, {self.puntos} p Interes', suave_con_keypoints)
        cv2.imshow(f'negra, {self.puntos} p Interes', negra_con_keypoints)
        if self.cany:
            cv2.imshow(f'bordes Canny', bordes)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return negra_con_keypoints

    def recortar(self,img):
        recortes_existentes = len(os.listdir("Encontrados"))
        original = cv2.resize(cv2.imread(self.path),(400,400))
        _, imagen_binarizada = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        # Encontrar los contornos en la imagen binarizada
        contornos, _ = cv2.findContours(imagen_binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        recortes = []
        # Recorrer los contornos y obtener el recorte de la figura binarizada
        for contorno in contornos:
            # Obtener las coordenadas del rectángulo del contorno
            x, y, w, h = cv2.boundingRect(contorno)

            # Recortar la figura binarizada utilizando las coordenadas del rectángulo
            figura_recortada = original[y:y+h, x:x+w]

            recortes.append(figura_recortada)
        
        #escribir en la carpeta
        if not os.path.exists(self.carpeta):
            os.mkdir(self.carpeta)
        
        for indice in range(len(recortes)):
            cv2.imshow(f"recorte {indice}",recortes[indice])
            if self.cany:
                cv2.imwrite(f"Encontrados/{recortes_existentes+1}_canny.jpg",recortes[indice])
            else:
                cv2.imwrite(f"Encontrados/{recortes_existentes+1}.jpg",recortes[indice])
            recortes_existentes+=1
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def circulos(self,agrupar=False):
        original = cv2.resize(cv2.imread(self.path),(400,400))
        negra_con_keypoints = cv2.cvtColor(self.keys(),cv2.COLOR_BGR2GRAY)
        
        #encontramos los circulos [N=>(x,y,r)]
        if agrupar:
            circles = cv2.HoughCircles(negra_con_keypoints, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=70, param2=30, minRadius=5, maxRadius=100) #si funciona
            # circles = cv2.HoughCircles(negra_con_keypoints, cv2.HOUGH_GRADIENT, dp=1, minDist=40, param1=50, param2=25, minRadius=5, maxRadius=100)
        else:
            circles = cv2.HoughCircles(negra_con_keypoints, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=30, param2=30, minRadius=5, maxRadius=90)

        circulos = np.zeros_like(negra_con_keypoints)
        # Si se detectaron círculos, dibujarlos en la imagen original

        if circles is not None:
            circles = np.round(circles[0, :]).astype(int)
            for (x, y, r) in circles:
                if r>20:
                    cv2.circle(circulos, (x, y), r, (255, 255, 255),-1)
                

        # Mostrar la imagen con los círculos detectados
        cv2.imshow("Circulos evaluados",negra_con_keypoints)
        cv2.imshow("original con circulos", circulos)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.recortar(circulos)
