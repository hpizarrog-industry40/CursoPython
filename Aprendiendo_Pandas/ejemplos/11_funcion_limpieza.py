# 11 - Automatizar la limpieza con funciones reutilizables
#
# Objetivo: convertir los pasos del ejemplo 10 en funciones pequenas,
# combinarlas en un flujo (pipeline) y reutilizarlo con cualquier archivo
# que tenga los mismos problemas.
#
# Regla practica: si repites un paso de limpieza mas de dos veces,
# conviertelo en una funcion.

import unicodedata

import pandas as pd


# ---------------------------------------------------------------------------
# Funciones pequenas: cada una hace UNA cosa y devuelve un DataFrame nuevo
# ---------------------------------------------------------------------------
def limpiar_nombres_columnas(df, renombrar=None):
    """Columnas en minuscula, sin espacios extremos, sin '(%)', con '_'.
    'renombrar' es un diccionario opcional para alinear con otra tabla."""
    df = df.copy()
    df.columns = (df.columns.str.strip()
                  .str.lower()
                  .str.replace(r"\s*\(%\)", "", regex=True)
                  .str.replace(" ", "_"))
    if renombrar:
        df = df.rename(columns=renombrar)
    return df


def quitar_tildes(texto):
    if not isinstance(texto, str):
        return texto
    return "".join(c for c in unicodedata.normalize("NFKD", texto)
                   if not unicodedata.combining(c))


def estandarizar_categoria(df, columna, mapeo=None):
    """Quita espacios y tildes, aplica un mapeo opcional y deja Formato Titulo."""
    df = df.copy()
    serie = df[columna].str.strip().str.lower().apply(quitar_tildes)
    if mapeo:
        serie = serie.replace(mapeo)
    df[columna] = serie.str.title()
    return df


def convertir_a_numero(df, columnas):
    """Convierte texto como '7,5', '95%', 'N/A' o '-' en numeros (o NaN)."""
    df = df.copy()
    for col in columnas:
        texto = (df[col].astype(str)
                 .str.replace(",", ".", regex=False)
                 .str.replace("%", "", regex=False)
                 .str.strip())
        df[col] = pd.to_numeric(texto, errors="coerce")
    return df


def quitar_duplicados(df):
    return df.drop_duplicates().reset_index(drop=True)


# ---------------------------------------------------------------------------
# Flujo completo: encadena las funciones con .pipe() y guarda un registro
# ---------------------------------------------------------------------------
MAPEO_CURSOS = {"mate": "matematicas", "fis.": "fisica"}
RENOMBRAR = {"nota_parcial_1": "nota_parcial1", "nota_parcial_2": "nota_parcial2"}
COLUMNAS_NUMERICAS = ["nota_parcial1", "nota_parcial2", "nota_final", "asistencia"]


def limpiar_datos(df, mapeo_cursos=MAPEO_CURSOS):
    """Aplica todo el flujo de limpieza y devuelve (df_limpio, registro)."""
    registro = {"filas_entrada": len(df)}

    limpio = (df.pipe(limpiar_nombres_columnas, RENOMBRAR)
                .pipe(quitar_duplicados)
                .pipe(estandarizar_categoria, "curso", mapeo_cursos)
                .pipe(estandarizar_categoria, "ciudad")
                .pipe(convertir_a_numero, COLUMNAS_NUMERICAS))
    limpio["nombre"] = limpio["nombre"].str.strip().str.replace(r"\s+", " ", regex=True).str.title()

    registro["duplicados_eliminados"] = registro["filas_entrada"] - len(limpio)
    registro["filas_salida"] = len(limpio)
    registro["faltantes"] = limpio.isnull().sum()[lambda s: s > 0].to_dict()
    return limpio, registro


if __name__ == "__main__":
    sucio = pd.read_csv("datos/alumnos_sucio.csv")
    limpio, registro = limpiar_datos(sucio)

    print("Registro de la limpieza:")
    for clave, valor in registro.items():
        print(f"  {clave}: {valor}")
    print()
    print("Cursos:", limpio["curso"].value_counts().to_dict())
    print("Ciudades:", limpio["ciudad"].value_counts().to_dict())
    print()
    print(limpio.head())

    # Comprobacion: el resultado debe parecerse al archivo limpio original
    original = pd.read_csv("datos/alumnos.csv")
    iguales = (limpio.sort_values("id")["nota_final"].values ==
               original.sort_values("id")["nota_final"].values).all()
    print("\nnota_final coincide con datos/alumnos.csv:", iguales)

    # Exportar el resultado
    limpio.to_csv("datos/alumnos_limpio.csv", index=False)
    print("Guardado en datos/alumnos_limpio.csv")
