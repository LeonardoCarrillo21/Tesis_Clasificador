import cv2
import numpy as np

# Cargar la imagen en escala de grises
image = cv2.imread('imgfrecu/O_12596.jpg', cv2.IMREAD_GRAYSCALE)

# Aplicar la Transformada de Fourier
frequencies = np.fft.fft2(image)

# Desplazar las frecuencias al centro de la imagen
shifted_frequencies = np.fft.fftshift(frequencies)

# Calcular el espectro de amplitud (magnitud) de las frecuencias
magnitude_spectrum = np.abs(shifted_frequencies)

# Dividir la imagen en subregiones o bandas de frecuencia
# Puedes ajustar estos valores según tus necesidades
num_rows, num_cols = image.shape
block_size = 16

energy_matrices = []

for row_start in range(0, num_rows, block_size):
    for col_start in range(0, num_cols, block_size):
        row_end = row_start + block_size
        col_end = col_start + block_size

        # Obtener la submatriz de magnitud del espectro de amplitud
        submatrix = magnitude_spectrum[row_start:row_end, col_start:col_end]

        # Calcular la energía de la submatriz
        energy = np.sum(submatrix ** 2)

        # Agregar la energía a la matriz de energía
        energy_matrices.append(energy)

# Convertir la lista de energías a una matriz
energy_matrices = np.array(energy_matrices)

# Calcular el número de columnas en la matriz de energía
num_energy_cols = num_cols // block_size
num_energy_rows = len(energy_matrices) // num_energy_cols

# Redimensionar la matriz de energía
energy_matrices = energy_matrices[:num_energy_rows * num_energy_cols].reshape(num_energy_rows, num_energy_cols)

print(energy_matrices)

