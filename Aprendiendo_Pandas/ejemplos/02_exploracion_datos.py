# 02 - Exploracion de datos
#
# Objetivo: conocer los metodos mas usados para entender un DataFrame
# antes de trabajar con el.

import pandas as pd

df = pd.read_csv("datos/alumnos.csv")

# info() muestra tipos de datos, cantidad de valores no nulos y memoria usada
print("Informacion general del DataFrame:")
df.info()
print()

# describe() genera estadisticas (media, min, max, etc.) de columnas numericas
print("Estadisticas descriptivas:")
print(df.describe())
print()

# dtypes muestra el tipo de dato de cada columna
print("Tipos de dato por columna:")
print(df.dtypes)
print()

# nunique() cuenta valores distintos por columna
print("Valores distintos por columna:")
print(df.nunique())
print()

# value_counts() cuenta cuantas veces aparece cada valor en una columna
print("Cantidad de alumnos por curso:")
print(df["curso"].value_counts())
