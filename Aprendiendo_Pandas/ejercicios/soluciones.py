# Soluciones de los ejercicios propuestos (uso del profesor)

import pandas as pd

df = pd.read_csv("../datos/alumnos.csv")


def ejercicio_1_alumnos_aprobados(df):
    return df[df["nota_final"] >= 5]


def ejercicio_2_promedio_por_curso(df):
    return df.groupby("curso")["nota_final"].mean()


def ejercicio_3_alumno_mejor_nota(df):
    return df.loc[df["nota_final"].idxmax(), "nombre"]


def ejercicio_4_contar_por_ciudad(df):
    return df["ciudad"].value_counts()


def ejercicio_5_nueva_columna_estado(df):
    df = df.copy()
    df["estado"] = df["nota_final"].apply(lambda n: "Aprobado" if n >= 5 else "Suspenso")
    return df


if __name__ == "__main__":
    print("Ejercicio 1 - Aprobados:")
    print(ejercicio_1_alumnos_aprobados(df))
    print()

    print("Ejercicio 2 - Promedio por curso:")
    print(ejercicio_2_promedio_por_curso(df))
    print()

    print("Ejercicio 3 - Mejor alumno:")
    print(ejercicio_3_alumno_mejor_nota(df))
    print()

    print("Ejercicio 4 - Alumnos por ciudad:")
    print(ejercicio_4_contar_por_ciudad(df))
    print()

    print("Ejercicio 5 - Columna 'estado':")
    print(ejercicio_5_nueva_columna_estado(df))
