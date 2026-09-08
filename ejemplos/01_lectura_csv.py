# 01 - Lectura de un archivo CSV con pandas
#
# Objetivo: aprender a cargar un CSV en un DataFrame y hacer una primera
# inspeccion basica de los datos.

import pandas as pd

# read_csv() lee el archivo y lo convierte en un DataFrame (una tabla)
df = pd.read_csv("datos/alumnos.csv")

print("Tipo de objeto:", type(df))
print()

# head(n) muestra las primeras n filas (por defecto 5)
print("Primeras 5 filas:")
print(df.head())
print()

# tail(n) muestra las ultimas n filas
print("Ultimas 3 filas:")
print(df.tail(3))
print()

# shape indica (numero_de_filas, numero_de_columnas)
print("Dimensiones (filas, columnas):", df.shape)
print()

# columns muestra el nombre de cada columna
print("Columnas:", list(df.columns))
