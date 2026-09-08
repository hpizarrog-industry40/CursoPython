# 07 - Ordenar datos y exportar resultados
#
# Objetivo: ordenar un DataFrame y guardar los resultados en un nuevo CSV.

import pandas as pd

df = pd.read_csv("datos/alumnos.csv")

# sort_values() ordena por una columna (ascending=False para descendente)
print("Alumnos ordenados por nota_final (de mayor a menor):")
df_ordenado = df.sort_values(by="nota_final", ascending=False)
print(df_ordenado[["nombre", "curso", "nota_final"]])
print()

# Se puede ordenar por varias columnas a la vez
print("Ordenado por curso (A-Z) y luego por nota_final (mayor a menor):")
df_ordenado_multi = df.sort_values(by=["curso", "nota_final"], ascending=[True, False])
print(df_ordenado_multi[["nombre", "curso", "nota_final"]])
print()

# to_csv() exporta el DataFrame resultante a un nuevo archivo CSV
salida = "datos/alumnos_ordenados.csv"
df_ordenado.to_csv(salida, index=False)
print(f"Resultado guardado en: {salida}")
