# 03 - Seleccion y filtrado de datos
#
# Objetivo: aprender a seleccionar columnas, filas y a filtrar con condiciones.

import pandas as pd

df = pd.read_csv("datos/alumnos.csv")

# Seleccionar UNA columna devuelve una Series
print("Columna 'nombre' (Series):")
print(df["nombre"].head())
print()

# Seleccionar VARIAS columnas devuelve un DataFrame (usar doble corchete)
print("Columnas 'nombre' y 'nota_final':")
print(df[["nombre", "nota_final"]].head())
print()

# loc[] selecciona por etiqueta (nombre de fila/columna)
print("Fila con indice 0 usando loc:")
print(df.loc[0])
print()

# iloc[] selecciona por posicion numerica
print("Primeras 3 filas, primeras 2 columnas usando iloc:")
print(df.iloc[0:3, 0:2])
print()

# Filtrado con condiciones booleanas
print("Alumnos con nota_final mayor o igual a 8:")
print(df[df["nota_final"] >= 8])
print()

# Combinar condiciones: & (y), | (o). Cada condicion entre parentesis.
print("Alumnos de Matematicas con asistencia mayor a 90:")
print(df[(df["curso"] == "Matematicas") & (df["asistencia"] > 90)])
