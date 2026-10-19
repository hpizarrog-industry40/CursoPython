# Soluciones de los ejercicios guiados - Parte 4 (uso del profesor)
#
#     cd ejercicios
#     python soluciones_parte4.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBRegressor


def ejercicio_1_crear_objetivo(df):
    df = df.copy()
    df["reprueba"] = (df["nota_final"] < 5).astype(int)              # 56 de 150
    return df


def ejercicio_2_entrenar_arbol(X_train, y_train):
    return DecisionTreeClassifier(max_depth=3, random_state=42).fit(X_train, y_train)


def ejercicio_3_random_forest(X_train, y_train):
    return RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)


def ejercicio_4_crear_rezagos(semanal):
    df = semanal.sort_values(["id", "semana"]).copy()
    g = df.groupby("id")["nota_control"]
    df["nota_lag1"] = g.shift(1)
    df["nota_media3"] = g.transform(lambda s: s.shift(1).rolling(3).mean())
    return df


def ejercicio_5_forecast_xgboost(df, variables):
    datos = df.dropna(subset=variables)
    train = datos[datos["semana"] <= 12]
    test = datos[datos["semana"] >= 13]
    modelo = XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=42)
    modelo.fit(train[variables], train["nota_control"])
    return mean_absolute_error(test["nota_control"], modelo.predict(test[variables]))


if __name__ == "__main__":
    import ejercicios_parte4 as ej

    for nombre in ["ejercicio_1_crear_objetivo", "ejercicio_2_entrenar_arbol",
                   "ejercicio_3_random_forest", "ejercicio_4_crear_rezagos",
                   "ejercicio_5_forecast_xgboost"]:
        setattr(ej, nombre, globals()[nombre])

    for n, t in enumerate([ej.test_1, ej.test_2, ej.test_3, ej.test_4, ej.test_5], start=1):
        ej.comprobar(n, t)
