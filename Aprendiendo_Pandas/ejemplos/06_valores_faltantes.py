# 06 - Valores faltantes (NaN)
#
# Objetivo: detectar y tratar datos faltantes. El CSV de ejemplo tiene
# valores vacios a proposito en 'nota_parcial2' y 'ciudad'.

import pandas as pd

df = pd.read_csv("datos/alumnos.csv")

# isnull() / isna() marcan con True donde hay un valor faltante
print("Cantidad de valores faltantes por columna:")
print(df.isnull().sum())
print()

# Filtrar filas que tienen algun valor faltante
print("Filas con algun dato faltante:")
print(df[df.isnull().any(axis=1)])
print()

# fillna() rellena los valores faltantes
# Ejemplo: rellenar 'nota_parcial2' con el promedio de esa columna
df_relleno = df.copy()
promedio_parcial2 = df_relleno["nota_parcial2"].mean()
df_relleno["nota_parcial2"] = df_relleno["nota_parcial2"].fillna(promedio_parcial2)
print(f"'nota_parcial2' rellenada con el promedio ({promedio_parcial2:.2f}):")
print(df_relleno[["nombre", "nota_parcial2"]])
print()

# Rellenar texto faltante con un valor fijo
df_relleno["ciudad"] = df_relleno["ciudad"].fillna("Desconocida")
print("'ciudad' rellenada con 'Desconocida':")
print(df_relleno[["nombre", "ciudad"]])
print()

# dropna() elimina filas (o columnas) con valores faltantes
df_sin_nulos = df.dropna()
print(f"Filas originales: {len(df)} -> Filas tras dropna(): {len(df_sin_nulos)}")
