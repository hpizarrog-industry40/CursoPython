# 04 - Operaciones con columnas
#
# Objetivo: crear, modificar y eliminar columnas; aplicar funciones.

import pandas as pd

df = pd.read_csv("datos/alumnos.csv")

# Crear una columna nueva a partir de otras (promedio de los 2 parciales)
df["promedio_parciales"] = (df["nota_parcial1"] + df["nota_parcial2"]) / 2
print("Nueva columna 'promedio_parciales':")
print(df[["nombre", "nota_parcial1", "nota_parcial2", "promedio_parciales"]].head())
print()

# Crear una columna condicional con apply() y una funcion
def clasificar(nota):
    if nota >= 9:
        return "Sobresaliente"
    elif nota >= 7:
        return "Notable"
    elif nota >= 5:
        return "Aprobado"
    else:
        return "Suspenso"

df["calificacion"] = df["nota_final"].apply(clasificar)
print("Columna 'calificacion' calculada con apply():")
print(df[["nombre", "nota_final", "calificacion"]].head())
print()

# rename() para cambiar el nombre de una columna
df = df.rename(columns={"ciudad": "ciudad_residencia"})
print("Columna 'ciudad' renombrada a 'ciudad_residencia':")
print(df.columns.tolist())
print()

# drop() para eliminar una columna (axis=1 = columnas)
df_sin_asistencia = df.drop(columns=["asistencia"])
print("DataFrame sin la columna 'asistencia':")
print(df_sin_asistencia.columns.tolist())
