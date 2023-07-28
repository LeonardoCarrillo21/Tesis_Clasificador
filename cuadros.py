import cv2
import random as rd
'''
    author: LEONARDO CARRILLO MARTINEZ
    PROGRAMA PARA GENERAR CUADROS ALEATORIOS EN UNA IMAGEN Y GENERAR RECORTES
'''
'''
    METODO DE USO
    crear objeto de la clase Cuadros()
    objeto = Cuadros()
    mandar a llamar a la funcion generaCuadros del objeto
    objeto.generaCuadros( !!COPIA DE LA IMAGEN¡¡¡ , Cantidad de recortes deseados )
'''

class Cuadros:
    
    def __init__(self):
        pass

    def mostrarYEsperar(self,nombres,imagenes):
        '''
        Descipcion de la funcion.
        muestra un conjunto de imagenes con su respectivo nombre

        Parámetros de la funcion.
        parametro1: vector de nombres de imagenes.
        parametro2: vector de imagenes a mostrar.
        
        Valor de retorno.
        None
        
        Ejemplo de uso.
        mostrarYEsperar(["nombre1","nombre2"],[imagen1,imagen2])
        '''
        for nombre,imagen in zip(nombres,imagenes):
            cv2.imshow(nombre,imagen)
            cv2.waitKey(0)
        cv2.destroyAllWindows()

    def generadorCuadros(self,img,cantidadCuadros):
        """
        Descripción de la función.

        generar recortes menores al tamaño de la imagen (400x400)
        generar coordenadas donde se ubicará cada cuadro
        cada coordenada deberá generarse aleatoriamente
        rango de generacion: [mitadCuadro-400-mitadCuadro] simulando un margen seguro de ubicacion
        ubicar la coordenada del cuadro la cual será el centro de cada cuadro
        ( opcional ) pintar y motrar la imagen con los cuadros aleatorios
        generar los recortes de la imagen:
        ( opcional )mostrar los recortes 

        Parámetros:
        - parametro1: copia de la imagen a generar cuadros, !!si no se envia una copia se edita la original.
        - parametro2: cantidad de cuadros a esperar.

        Valor de retorno:
        - retorna una lista de imagenes que corresponden a la cantidad de recortes.

        Ejemplo de uso:
        >> mi_funcion(imagen.copy(), 20)
        retorna: [recorteImagen1,recorteImagen2,recorteImagen3]
        """
            
        #generar los cuadros aleatoriamente
        listaCuadros= [(rd.randint(2,398),rd.randint(2,398)) for i in range(cantidadCuadros)]
        listaSecciones=[]

        #obtener las ubicaciones de los cuadros y las coordenadas de sus vertices
        # x,y centro del cuadro
        #x1,y1 coordenadas del punto superior izquierda
        #x2,y2 coordenadas del punto inferior derecha
        #los pares x1,x2 representan los 
        for cuadro in listaCuadros:
            mitadAncho = int(cuadro[1]/2)
            mitadAlto = int(cuadro[0]/2)
            x = rd.randint(mitadAncho,400-mitadAncho)
            y = rd.randint(mitadAlto,400-mitadAlto)
            x1,y1,x2,y2= x-mitadAncho,y-mitadAlto,x+mitadAncho,y+mitadAlto
            
            listaSecciones.append((x1,y1,x2,y2))
        rectangulos = img.copy()
        
        #mostrar los cuadros en la imagen original (OPCIONAL)
        #<<<<<<<<<<<<OPCIONAL>>>>>>>>>>>>>>>>>
        for seccion in listaSecciones:
            cv2.rectangle(rectangulos,(seccion[0],seccion[1]),(seccion[2],seccion[3]),color=(0,0,255),thickness=1)
        cv2.imshow("rectangulos",rectangulos)
        cv2.waitKey()
        cv2.destroyAllWindows()
        #<<<<<<<<<<<<------------>>>>>>>>>>>>>>>>>

        #generar los "cantidadCuadros" recortes
        recortes = [img[seccion[1]:seccion[3],seccion[0]:seccion[2]] for seccion in listaSecciones]

        #mostrar los recortes
        #<<<<<<<<<<<<OPCIONAL>>>>>>>>>>>>>>>>>
        arr = range(len(recortes))
        nombres = [f'recorte {str(i)}' for i in arr]
        self.mostrarYEsperar(nombres,recortes)
        #<<<<<<<<<<<<------------>>>>>>>>>>>>>>>>>
        return recortes

    def ejemplo(self):
        path = "botellas descargadas/5.jpg" #cambiar ruta de imagen
        imagen = cv2.imread(path,0)
        imagen = cv2.resize(imagen,(400,400))
        self.generadorCuadros(imagen.copy(),self.cuadros)

# Cuadros().ejemplo()