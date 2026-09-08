# Ejercicios propuestos
#
# Completa cada funcion usando lo aprendido en la carpeta ejemplos/.
# Ejecuta este archivo al final para comprobar tus respuestas.

import pandas as pd

df = pd.read_csv("../datos/alumnos.csv")


def ejercicio_1_alumnos_aprobados(df):
    """Devuelve un DataFrame solo con los alumnos con nota_final >= 5."""
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_2_promedio_por_curso(df):
    """Devuelve una Series con el promedio de nota_final por curso."""
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_3_alumno_mejor_nota(df):
    """Devuelve el nombre del alumno con la nota_final mas alta."""
    # TODO: escribe tu codigo aqui (pista: usa sort_values o idxmax)
    pass


def ejercicio_4_contar_por_ciudad(df):
    """Devuelve cuantos alumnos hay por cada ciudad (usa value_counts)."""
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_5_nueva_columna_estado(df):
    """
    Agrega una columna 'estado' que valga 'Aprobado' si nota_final >= 5,
    y 'Suspenso' en caso contrario. Devuelve el DataFrame con la columna nueva.
    """
    # TODO: escribe tu codigo aqui
    pass


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
