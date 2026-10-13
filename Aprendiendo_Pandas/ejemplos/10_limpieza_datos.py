# 10 - Limpieza de datos reales, paso a paso
#
# Objetivo: tomar un archivo "sucio" (como los que llegan desde planillas
# o sistemas reales) y dejarlo listo para analizar.
#
# Problemas que tiene datos/alumnos_sucio.csv:
#   - Nombres de columna con espacios, mayusculas y simbolos.
#   - Categorias escritas de muchas formas: "FISICA", "Física", "Fis.".
#   - Ciudades en mayusculas/minusculas y con espacios.
#   - Notas como texto con coma decimal ("7,5") y marcas "N/A" o "-".
#   - Asistencia con el simbolo "%".
#   - Filas duplicadas.

import unicodedata

import pandas as pd

df = pd.read_csv("datos/alumnos_sucio.csv")
print("Columnas originales:", list(df.columns))
print("Filas:", len(df))
print(df.dtypes)
print()

# ---------------------------------------------------------------------------
# 1. Nombres de columnas: sin espacios, minusculas, sin simbolos
# ---------------------------------------------------------------------------
df.columns = (df.columns.str.strip()
              .str.lower()
              .str.replace(r"\s*\(%\)", "", regex=True)
              .str.replace(" ", "_"))

# Alinear con los nombres de la base principal (datos/alumnos.csv),
# para poder unir o comparar ambas tablas despues.
df = df.rename(columns={"nota_parcial_1": "nota_parcial1",
                        "nota_parcial_2": "nota_parcial2"})
print("Columnas limpias:", list(df.columns))
print()

# ---------------------------------------------------------------------------
# 2. Filas duplicadas
# ---------------------------------------------------------------------------
print("Filas duplicadas:", df.duplicated().sum())
df = df.drop_duplicates()
print("Filas tras drop_duplicates():", len(df))
print()

# ---------------------------------------------------------------------------
# 3. Texto: espacios sobrantes y mayusculas
# ---------------------------------------------------------------------------
df["nombre"] = (df["nombre"].str.strip()
                .str.replace(r"\s+", " ", regex=True)   # "Carlos  Ruiz" -> "Carlos Ruiz"
                .str.title())
df["ciudad"] = df["ciudad"].str.strip().str.title()
print("Ciudades:", df["ciudad"].value_counts(dropna=False).to_dict())
print()

# ---------------------------------------------------------------------------
# 4. Estandarizar categorias de curso
# ---------------------------------------------------------------------------
print("Variantes de curso ANTES:", df["curso"].nunique())
print(df["curso"].value_counts())


def quitar_tildes(texto):
    """'Física' -> 'Fisica'."""
    return "".join(c for c in unicodedata.normalize("NFKD", texto)
                   if not unicodedata.combining(c))


df["curso"] = df["curso"].str.strip().str.lower().apply(quitar_tildes)

# Abreviaturas que no se resuelven solo con minusculas: diccionario de mapeo.
mapeo = {"mate": "matematicas", "fis.": "fisica"}
df["curso"] = df["curso"].replace(mapeo).str.title()
print("Variantes de curso DESPUES:", df["curso"].nunique())
print(df["curso"].value_counts())
print()

# ---------------------------------------------------------------------------
# 5. Numeros guardados como texto
# ---------------------------------------------------------------------------
for col in ["nota_parcial1", "nota_parcial2", "nota_final"]:
    df[col] = (df[col].astype(str)
               .str.replace(",", ".", regex=False)
               .replace({"N/A": None, "-": None, "nan": None}))
    # errors="coerce" convierte en NaN cualquier valor que no sea numero
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["asistencia"] = pd.to_numeric(df["asistencia"].str.replace("%", ""), errors="coerce")
print("Tipos despues de convertir:")
print(df.dtypes)
print()

# ---------------------------------------------------------------------------
# 6. Validacion final
# ---------------------------------------------------------------------------
print("Faltantes por columna:")
print(df.isnull().sum())
assert df["id"].is_unique, "Hay ids repetidos"
assert df["nota_final"].between(0, 10).all(), "Notas fuera de rango"
print("Validaciones OK. Filas finales:", len(df))
