import cv2
import numpy as np

# Cargar la imagen en escala de grises
image = cv2.imread('botellas_descargadas/20.jpg', 0)
image = cv2.resize(image,(400,400))
# Definir las máscaras de Roberts
mask_diagonal = np.array([[1, 0], [0, -1]], dtype=np.float32)
mask_horizontal_vertical = np.array([[0, 1], [-1, 0]], dtype=np.float32)

# Aplicar las máscaras de Roberts
gradient_diagonal = cv2.filter2D(image, -1, mask_diagonal)
gradient_horizontal_vertical = cv2.filter2D(image, -1, mask_horizontal_vertical)

# Calcular la magnitud del gradiente
gradient_magnitude = cv2.magnitude(gradient_diagonal, gradient_horizontal_vertical)

# Mostrar las imágenes resultantes
cv2.imshow('Original', image)
cv2.imshow('Gradient Diagonal', gradient_diagonal)
cv2.imshow('Gradient Horizontal/Vertical', gradient_horizontal_vertical)
cv2.imshow('Gradient Magnitude', gradient_magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()
