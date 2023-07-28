import cv2
import numpy as np
# rutaImagen = "plastic/plastic381.jpg"
rutaImagen = "plastic/plastic49.jpg"
orbe = cv2.ORB_create()

def pintarPuntos(imagen,puntos):
    return cv2.drawKeypoints(imagen, puntos, None, color=(0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

def suave(image,veces):
        #se suavisa
        for i in range(veces):
            image = cv2.GaussianBlur(image, (5, 5), 0)
        return image

def mostrarYEsperar(imagenes,nombres):
    for imagen,nombre in zip(imagenes,nombres):
        cv2.imshow(nombre,imagen)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

def ordenarPuntos(puntos):
    # keypoints_ordenado = sorted(keypoints, key=lambda kp: kp.response, reverse=True)
    return sorted(puntos, clave=lambda kp: kp.response)


def separarPuntosTamaño(puntos):
    diccionario = {}
    for punto in puntos:
        if not punto.size in diccionario:
            diccionario[punto.size] = []
        diccionario[punto.size].append(punto)
    return diccionario

def separarVectorPartesIguales(vector,tam):
    elementos = len(vector)
    vectoresResultantes = []
    secciones = int(elementos/tam)
    ultimaSeccion = int(elementos%tam)
    for i in range(secciones):
        vectoresResultantes.append(vector[i*tam:i*tam+tam])
    vectoresResultantes.append(vector[secciones*tam:secciones*tam+ultimaSeccion])
    return vectoresResultantes

def analisisTamanioPuntos(imagen):
    puntos, descriptores = orbe.detectAndCompute(imagen,None)
    print(f'cantidad de puntos: {len(puntos)}')
    # print(f'tamPuntos: {[punto.size for punto in puntos]}')
    # print(f'octava: {[punto.octave for punto in puntos]}')
    # print(f'class id:  {[punto.class_id for punto in puntos]}')
    pintada = pintarPuntos(imagen,puntos)
    puntosSeparadosTam = separarPuntosTamaño(puntos)
    imagenesConPuntosSeparados = [pintarPuntos(imagen,puntosSeparadosTam[tamanio]) for tamanio in puntosSeparadosTam]
    mostrarYEsperar(imagenesConPuntosSeparados,[str(tamanio) for tamanio in puntosSeparadosTam])

def analisisRespuesta(imagen):
    rangoImportantes = 10
    puntos, descriptores = orbe.detectAndCompute(imagen,None)
    print(f'cantidad de puntos: {len(puntos)}')
    # print(f'respuesta:{[punto.response for punto in puntos]}')
    puntosOrdenadosImportancia = sorted(puntos, key=lambda kp: kp.response, reverse=True)
    puntosPorRango = separarVectorPartesIguales(puntosOrdenadosImportancia,20)

    imagenesPintadas = [pintarPuntos(imagen,vector) for vector in puntosPorRango]
    cantidad = list(range(len(puntosPorRango)))
    nombres = [str(nom) for nom in cantidad]
    mostrarYEsperar(nombres,[imagenesPintadas])

imagen = cv2.imread(rutaImagen)
# analisisTamanioPuntos(imagen)
analisisRespuesta(imagen)