import pandas as pd

datos = pd.Series([12, 25, 37, 41, 53])

desviacion = datos.std()
print("Desviación estándar: ", desviacion)

varianza = datos.var()
print("Varianza:", varianza)

cantidad = datos.count()
suma = datos.sum()
print("Cantidad de datos:", cantidad)
print("Suma total:", suma)

elementos = datos.size
print("Cantidad total de elementos:", elementos)