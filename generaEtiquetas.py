arreglo = ['uno', 'dos', 'tres', 'uno','dos','dos']

elementos = len(arreglo)  # Paso 1
etiquetas = list(set(arreglo))  # Obtener etiquetas únicas sin repetir
L = len(etiquetas)  # Tamaño de las etiquetas únicas

C = len(etiquetas)  # Tamaño de las columnas de la matriz
matriz = [[0] * C for _ in range(elementos)]  # Inicializar matriz con ceros

for i, elemento in enumerate(arreglo):
    indice = etiquetas.index(elemento)  # Obtener índice de la etiqueta
    matriz[i][indice] = 1  # Asignar 1 en la posición correspondiente

print(matriz)
