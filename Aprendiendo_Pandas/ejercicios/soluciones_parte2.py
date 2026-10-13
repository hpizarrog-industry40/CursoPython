# Soluciones de los ejercicios - Parte 2 (uso del profesor)
#
# Se ejecutan con las mismas comprobaciones de ejercicios_parte2.py:
#
#     cd ejercicios
#     python soluciones_parte2.py

import unicodedata

import pandas as pd

alumnos = pd.read_csv("../datos/alumnos.csv")
cursos = pd.read_csv("../datos/cursos.csv")
asistencia = pd.read_csv("../datos/asistencia_mensual.csv")
periodo2 = pd.read_csv("../datos/alumnos_2026_2.csv")
sucio = pd.read_csv("../datos/alumnos_sucio.csv")


def ejercicio_1_agregar_profesor(alumnos, cursos):
    # how="left" conserva los 20 alumnos; validate evita duplicados silenciosos
    return alumnos.merge(cursos, on="curso", how="left", validate="many_to_one")


def ejercicio_2_asistencia_promedio(alumnos, asistencia):
    # 1) Bajar la granularidad: de (id, mes) a (id)
    prom = (asistencia.groupby("id", as_index=False)["asistencia"].mean()
            .rename(columns={"asistencia": "asistencia_prom"}))
    # 2) Ahora si, unir 1 a 1
    return alumnos.merge(prom, on="id", how="left", validate="one_to_one")


def ejercicio_3_historico(alumnos, periodo2):
    return pd.concat([alumnos.assign(periodo="2026-1"),
                      periodo2.assign(periodo="2026-2")],
                     ignore_index=True)


def ejercicio_4_alumnos_que_no_continuan(alumnos, periodo2):
    cruce = alumnos.merge(periodo2[["id"]], on="id", how="left", indicator=True)
    return cruce.loc[cruce["_merge"] == "left_only", "nombre"].tolist()
    # Alternativa sin merge:
    # return alumnos.loc[~alumnos["id"].isin(periodo2["id"]), "nombre"].tolist()


def _quitar_tildes(texto):
    if not isinstance(texto, str):
        return texto
    return "".join(c for c in unicodedata.normalize("NFKD", texto)
                   if not unicodedata.combining(c))


def ejercicio_5_limpiar(sucio):
    df = sucio.copy()
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(r"\s*\(%\)", "", regex=True)
                  .str.replace(" ", "_"))
    df = df.rename(columns={"nota_parcial_1": "nota_parcial1",
                            "nota_parcial_2": "nota_parcial2"})
    df = df.drop_duplicates().reset_index(drop=True)

    df["curso"] = (df["curso"].str.strip().str.lower().apply(_quitar_tildes)
                   .replace({"mate": "matematicas", "fis.": "fisica"})
                   .str.title())
    df["ciudad"] = df["ciudad"].str.strip().str.title()

    for col in ["nota_parcial1", "nota_parcial2", "nota_final", "asistencia"]:
        texto = (df[col].astype(str).str.replace(",", ".", regex=False)
                 .str.replace("%", "", regex=False).str.strip())
        df[col] = pd.to_numeric(texto, errors="coerce")
    return df


if __name__ == "__main__":
    import ejercicios_parte2 as ej

    # Reemplaza las funciones vacias por las soluciones y corre los tests
    for nombre in ["ejercicio_1_agregar_profesor", "ejercicio_2_asistencia_promedio",
                   "ejercicio_3_historico", "ejercicio_4_alumnos_que_no_continuan",
                   "ejercicio_5_limpiar"]:
        setattr(ej, nombre, globals()[nombre])

    for n, t in enumerate([ej.test_1, ej.test_2, ej.test_3, ej.test_4, ej.test_5], start=1):
        ej.comprobar(n, t)

    print()
    print("Alumnos que no continuan:", ejercicio_4_alumnos_que_no_continuan(alumnos, periodo2))
