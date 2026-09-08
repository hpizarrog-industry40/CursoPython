# 05 - Agrupacion y agregacion (groupby)
#
# Objetivo: resumir datos agrupandolos por una o mas columnas.

import pandas as pd

df = pd.read_csv("datos/alumnos.csv")

# groupby + mean(): promedio de nota_final por curso
print("Nota final promedio por curso:")
print(df.groupby("curso")["nota_final"].mean())
print()

# groupby + varias agregaciones con agg()
print("Estadisticas de nota_final por curso:")
print(df.groupby("curso")["nota_final"].agg(["mean", "min", "max", "count"]))
print()

# Agrupar por mas de una columna
print("Promedio de asistencia por curso y ciudad:")
print(df.groupby(["curso", "ciudad"])["asistencia"].mean())
print()

# sort_values() para ordenar resultados
print("Cursos ordenados por nota_final promedio (de mayor a menor):")
promedios = df.groupby("curso")["nota_final"].mean().sort_values(ascending=False)
print(promedios)
