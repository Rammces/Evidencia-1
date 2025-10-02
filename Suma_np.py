import numpy as np

datos = np.array([6, 12, 18, 24, 30])
print("Datos:", datos)
print("Suma total:", np.sum(datos))

matriz = np.array([[10, 20, 30],
                   [5, 15, 25],
                   [2, 4, 6]])

print("\nMatriz:\n", matriz)
print("Suma total matriz:", np.sum(matriz))
print("Suma por filas:", np.sum(matriz, axis=1))
print("Suma por columnas:", np.sum(matriz, axis=0))