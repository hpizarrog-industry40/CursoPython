# Ejercicios propuestos - Parte 2
# Unidad 4: combinacion de tablas | Unidad 5: limpieza y automatizacion
#
# Completa cada funcion usando lo aprendido en los ejemplos 08 al 11.
# Ejecuta este archivo desde la carpeta ejercicios/:
#
#     cd ejercicios
#     python ejercicios_parte2.py
#
# Al final se ejecutan comprobaciones automaticas: cada ejercicio
# correcto muestra "OK".

import pandas as pd

alumnos = pd.read_csv("../datos/alumnos.csv")
cursos = pd.read_csv("../datos/cursos.csv")
asistencia = pd.read_csv("../datos/asistencia_mensual.csv")
periodo2 = pd.read_csv("../datos/alumnos_2026_2.csv")
sucio = pd.read_csv("../datos/alumnos_sucio.csv")


def ejercicio_1_agregar_profesor(alumnos, cursos):
    """
    Une alumnos con cursos para agregar las columnas profesor, sala y
    creditos. Debe conservar TODOS los alumnos (20 filas) y validar que la
    relacion sea muchos-a-uno.
    """
    # TODO: escribe tu codigo aqui (pista: merge con how y validate)
    pass


def ejercicio_2_asistencia_promedio(alumnos, asistencia):
    """
    asistencia tiene 3 filas por alumno (una por mes). Calcula la asistencia
    promedio de cada alumno y unela a la tabla alumnos en una columna
    llamada 'asistencia_prom'. El resultado debe seguir teniendo 20 filas.
    """
    # TODO: escribe tu codigo aqui (pista: groupby antes del merge)
    pass


def ejercicio_3_historico(alumnos, periodo2):
    """
    Apila los dos periodos en un solo DataFrame. Agrega una columna
    'periodo' con los valores '2026-1' (alumnos) y '2026-2' (periodo2).
    El indice debe ir de 0 a n-1.
    """
    # TODO: escribe tu codigo aqui (pista: assign + concat con ignore_index)
    pass


def ejercicio_4_alumnos_que_no_continuan(alumnos, periodo2):
    """
    Devuelve una lista con los NOMBRES de los alumnos que estaban en el
    periodo 1 pero NO aparecen en el periodo 2 (comparar por 'id').
    """
    # TODO: escribe tu codigo aqui (pista: merge con indicator=True)
    pass


def ejercicio_5_limpiar(sucio):
    """
    Limpia el archivo alumnos_sucio.csv y devuelve un DataFrame que cumpla:
      - columnas en minuscula y con '_' (nota_parcial1, nota_parcial2,
        nota_final, asistencia, ...)
      - sin filas duplicadas (20 filas)
      - curso con solo 3 valores: Matematicas, Fisica, Quimica
      - nota_final y asistencia numericas (float o int)
    """
    # TODO: escribe tu codigo aqui (pista: reutiliza las funciones del ejemplo 11)
    pass


# ---------------------------------------------------------------------------
# Comprobaciones automaticas (no modificar)
# ---------------------------------------------------------------------------
def comprobar(numero, funcion_test):
    try:
        funcion_test()
        print(f"Ejercicio {numero}: OK")
    except Exception as e:
        print(f"Ejercicio {numero}: pendiente o incorrecto -> {type(e).__name__}: {e}")


def test_1():
    r = ejercicio_1_agregar_profesor(alumnos, cursos)
    assert len(r) == 20 and "profesor" in r.columns
    assert r["profesor"].notna().all()


def test_2():
    r = ejercicio_2_asistencia_promedio(alumnos, asistencia)
    assert len(r) == 20 and "asistencia_prom" in r.columns
    assert abs(r.loc[r["id"] == 1, "asistencia_prom"].iloc[0] - 95) < 0.01


def test_3():
    r = ejercicio_3_historico(alumnos, periodo2)
    assert len(r) == 40 and set(r["periodo"]) == {"2026-1", "2026-2"}
    assert list(r.index) == list(range(40))


def test_4():
    r = ejercicio_4_alumnos_que_no_continuan(alumnos, periodo2)
    assert sorted(r) == ["Diego Fernandez", "Hugo Vega"]


def test_5():
    r = ejercicio_5_limpiar(sucio)
    assert len(r) == 20
    assert sorted(r["curso"].unique()) == ["Fisica", "Matematicas", "Quimica"]
    assert pd.api.types.is_numeric_dtype(r["nota_final"])
    assert pd.api.types.is_numeric_dtype(r["asistencia"])


if __name__ == "__main__":
    for n, t in enumerate([test_1, test_2, test_3, test_4, test_5], start=1):
        comprobar(n, t)
