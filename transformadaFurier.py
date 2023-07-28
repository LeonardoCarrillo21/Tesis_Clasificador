import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
def getFrecuenciaAmplitud(path):
    # Cargar la imagen en escala de grises
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Aplicar la Transformada de Fourier
    frequencies = np.fft.fft2(image)

    # Desplazar las frecuencias al centro de la imagen
    shifted_frequencies = np.fft.fftshift(frequencies)

    # Calcular el espectro de amplitud (magnitud) de las frecuencias
    magnitude_spectrum = 20 * np.log(np.abs(shifted_frequencies))

    # Mostrar la imagen original y el espectro de amplitud
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Imagen original'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Espectro de amplitud'), plt.xticks([]), plt.yticks([])
    plt.show()

def buscador(path):
    nombres = os.listdir(path)
    for nombre in nombres:
        getFrecuenciaAmplitud(path+"/"+nombre)

buscador("imagenes Frecuencias")