# Ejercicios guiados - Parte 3
# Unidad 6: uso estadistico con Python (regresion lineal simple y multiple)
#
# Completa cada funcion usando lo aprendido en los ejemplos 12 al 15.
# Cada ejercicio trae una GUIA paso a paso en su descripcion.
# Ejecuta este archivo desde la carpeta ejercicios/:
#
#     cd ejercicios
#     python ejercicios_parte3.py
#
# Requiere: pandas, statsmodels y scikit-learn (instalados en Google Colab).

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("../datos/rendimiento.csv")


def ejercicio_1_correlacion(df):
    """
    Devuelve el coeficiente de correlacion entre 'asistencia' y
    'nota_final', redondeado a 2 decimales.

    Guia:
      1. Selecciona la columna df["asistencia"].
      2. Usa el metodo .corr() pasandole df["nota_final"].
      3. Redondea con round(valor, 2).
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_2_regresion_simple(df):
    """
    Ajusta la regresion  nota_final ~ asistencia  con statsmodels y
    devuelve un diccionario con:
        {"intercepto": ..., "pendiente": ..., "r2": ...}
    (valores sin redondear).

    Guia:
      1. modelo = smf.ols("nota_final ~ asistencia", data=df).fit()
      2. modelo.params["Intercept"] y modelo.params["asistencia"]
      3. modelo.rsquared
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_3_predecir(df, asistencia):
    """
    Usando el modelo del ejercicio 2, devuelve la nota final predicha
    para un estudiante con la asistencia indicada (un numero).

    Guia:
      1. Ajusta (o reutiliza) el modelo del ejercicio 2.
      2. Crea un DataFrame con una columna "asistencia": [asistencia].
      3. Usa modelo.predict(...) y devuelve el primer valor como float.
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_4_regresion_multiple(df):
    """
    Ajusta el modelo
        nota_final ~ horas_estudio + asistencia + horas_sueno + C(trabaja)
    SOLO con las filas que no tienen faltantes en horas_sueno, y devuelve
    el modelo ajustado (el objeto que entrega .fit()).

    Guia:
      1. datos = df.dropna(subset=["horas_sueno"])
      2. smf.ols(formula, data=datos).fit()
      3. Revisa modelo.summary() para ver los resultados.
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_5_variables_no_significativas(modelo):
    """
    Recibe un modelo ajustado (por ejemplo, el del ejercicio 4) y devuelve
    una LISTA con los nombres de las variables cuyo p-valor es >= 0.05,
    sin incluir 'Intercept'.

    Guia:
      1. modelo.pvalues es una Series: indice = variable, valor = p-valor.
      2. Filtra los valores >= 0.05.
      3. Quita "Intercept" si aparece y convierte el indice a lista.
    """
    # TODO: escribe tu codigo aqui
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
    assert ejercicio_1_correlacion(df) == 0.61


def test_2():
    r = ejercicio_2_regresion_simple(df)
    assert abs(r["pendiente"] - 0.0958) < 0.001
    assert abs(r["intercepto"] - (-2.229)) < 0.01
    assert abs(r["r2"] - 0.371) < 0.001


def test_3():
    assert abs(ejercicio_3_predecir(df, 90) - 6.39) < 0.01


def test_4():
    m = ejercicio_4_regresion_multiple(df)
    assert int(m.nobs) == 146
    assert abs(m.params["horas_estudio"] - 0.303) < 0.01


def test_5():
    m = smf.ols("nota_final ~ horas_estudio + asistencia + horas_sueno + C(trabaja)",
                data=df.dropna(subset=["horas_sueno"])).fit()
    assert ejercicio_5_variables_no_significativas(m) == ["horas_sueno"]


if __name__ == "__main__":
    for n, t in enumerate([test_1, test_2, test_3, test_4, test_5], start=1):
        comprobar(n, t)
