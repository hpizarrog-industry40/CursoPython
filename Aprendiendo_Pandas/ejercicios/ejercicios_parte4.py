# Ejercicios guiados - Parte 4
# Unidad 7: modelos de prediccion con arboles (arbol de decision,
#           Random Forest y XGBoost) y forecasting semanal
#
# Completa cada funcion usando lo aprendido en los ejemplos 16 al 19.
# Cada ejercicio trae una GUIA paso a paso en su descripcion.
# Ejecuta este archivo desde la carpeta ejercicios/:
#
#     cd ejercicios
#     python ejercicios_parte4.py
#
# Requiere: pandas, scikit-learn y xgboost (instalados en Google Colab).
#
# Orden: los ejercicios 2 y 3 usan el resultado del 1; el 5 usa el del 4.

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_absolute_error, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBRegressor

rendimiento = pd.read_csv("../datos/rendimiento.csv")
semanal = pd.read_csv("../datos/seguimiento_semanal.csv")


def ejercicio_1_crear_objetivo(df):
    """
    Devuelve una COPIA de df con una columna nueva 'reprueba' que vale 1 si
    nota_final < 5 y 0 en caso contrario (numeros enteros).

    Guia:
      1. df = df.copy()
      2. (df["nota_final"] < 5) entrega True/False
      3. .astype(int) convierte True/False en 1/0
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_2_entrenar_arbol(X_train, y_train):
    """
    Entrena y devuelve un arbol de decision de profundidad maxima 3.

    Guia:
      1. DecisionTreeClassifier(max_depth=3, random_state=42)
      2. .fit(X_train, y_train)
      3. Devuelve el modelo entrenado
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_3_random_forest(X_train, y_train):
    """
    Entrena y devuelve un Random Forest de 200 arboles.

    Guia:
      1. RandomForestClassifier(n_estimators=200, random_state=42)
      2. .fit(X_train, y_train)
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_4_crear_rezagos(semanal):
    """
    Devuelve una COPIA de semanal, ordenada por id y semana, con dos columnas:
      - nota_lag1  : nota_control de la semana anterior del MISMO estudiante
      - nota_media3: promedio de nota_control de las 3 semanas anteriores
                     (sin incluir la semana actual)

    Guia:
      1. df = semanal.sort_values(["id", "semana"]).copy()
      2. g = df.groupby("id")["nota_control"]
      3. df["nota_lag1"] = g.shift(1)
      4. df["nota_media3"] = g.transform(lambda s: s.shift(1).rolling(3).mean())
    """
    # TODO: escribe tu codigo aqui
    pass


def ejercicio_5_forecast_xgboost(df, variables):
    """
    Entrena un XGBoost para pronosticar nota_control con DIVISION TEMPORAL y
    devuelve el error medio absoluto (MAE) en las semanas de prueba.

    Guia:
      1. datos = df.dropna(subset=variables)
      2. train = semanas <= 12 ; test = semanas >= 13   (¡nunca al azar!)
      3. XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05,
                      random_state=42).fit(train[variables], train["nota_control"])
      4. mean_absolute_error(test["nota_control"], modelo.predict(test[variables]))
    """
    # TODO: escribe tu codigo aqui
    pass


# ---------------------------------------------------------------------------
# Preparacion comun (no modificar)
# ---------------------------------------------------------------------------
def preparar_clasificacion():
    datos = ejercicio_1_crear_objetivo(rendimiento)
    X = pd.get_dummies(datos[["horas_estudio", "asistencia", "trabaja", "curso"]],
                       columns=["trabaja", "curso"], drop_first=True, dtype=int)
    y = datos["reprueba"]
    return train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


def preparar_forecasting():
    df = ejercicio_4_crear_rezagos(semanal)
    df = df.merge(rendimiento[["id", "trabaja"]], on="id", how="left")
    df["trabaja_si"] = (df["trabaja"] == "Si").astype(int)
    df["es_certamen"] = df["semana"].isin([8, 16]).astype(int)
    df["semanas_para_certamen"] = df["semana"].apply(lambda s: 8 - s if s <= 8 else 16 - s)
    variables = ["semanas_para_certamen", "es_certamen", "trabaja_si", "nota_lag1", "nota_media3"]
    return df, variables


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
    r = ejercicio_1_crear_objetivo(rendimiento)
    assert "reprueba" not in rendimiento.columns, "Debes trabajar sobre una copia"
    assert int(r["reprueba"].sum()) == 56


def test_2():
    X_train, X_test, y_train, y_test = preparar_clasificacion()
    m = ejercicio_2_entrenar_arbol(X_train, y_train)
    assert m.get_depth() <= 3
    assert abs(accuracy_score(y_test, m.predict(X_test)) - 0.867) < 0.01


def test_3():
    X_train, X_test, y_train, y_test = preparar_clasificacion()
    m = ejercicio_3_random_forest(X_train, y_train)
    assert len(m.estimators_) == 200
    assert abs(accuracy_score(y_test, m.predict(X_test)) - 0.889) < 0.01
    assert abs(recall_score(y_test, m.predict(X_test)) - 0.941) < 0.01


def test_4():
    r = ejercicio_4_crear_rezagos(semanal)
    fila = r[(r["id"] == 1) & (r["semana"] == 4)].iloc[0]
    assert fila["nota_lag1"] == 10.0
    assert abs(fila["nota_media3"] - 9.633) < 0.01
    assert r[r["semana"] == 1]["nota_lag1"].isna().all(), "La semana 1 no tiene semana anterior"


def test_5():
    df, variables = preparar_forecasting()
    mae = ejercicio_5_forecast_xgboost(df, variables)
    assert abs(mae - 0.629) < 0.01
    assert mae < 0.743, "Debe ganarle al pronostico ingenuo (MAE 0.743)"


if __name__ == "__main__":
    for n, t in enumerate([test_1, test_2, test_3, test_4, test_5], start=1):
        comprobar(n, t)
