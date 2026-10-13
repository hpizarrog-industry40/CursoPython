# 15 - Predecir y evaluar un modelo con datos nuevos (scikit-learn)
#
# Objetivo: comprobar si el modelo predice bien estudiantes que NO uso
# para aprender. Se separan los datos en entrenamiento y prueba.
#
# Requiere: pandas y scikit-learn (vienen instalados en Google Colab).
# En local:  pip install scikit-learn

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("datos/rendimiento.csv")

# ---------------------------------------------------------------------------
# 1. Variables explicativas (X) y variable a predecir (y)
# ---------------------------------------------------------------------------
# scikit-learn necesita solo numeros: las categorias se convierten en
# columnas 0/1 con get_dummies (drop_first evita una columna redundante).
X = pd.get_dummies(df[["horas_estudio", "asistencia", "trabaja", "curso"]],
                   columns=["trabaja", "curso"], drop_first=True, dtype=int)
y = df["nota_final"]
print("Columnas de X:", list(X.columns))
print()

# ---------------------------------------------------------------------------
# 2. Separar entrenamiento (80%) y prueba (20%)
# ---------------------------------------------------------------------------
# random_state fija el azar para que todos obtengan el mismo resultado.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)
print(f"Entrenamiento: {len(X_train)} filas | Prueba: {len(X_test)} filas")
print()

# ---------------------------------------------------------------------------
# 3. Entrenar y predecir
# ---------------------------------------------------------------------------
modelo = LinearRegression()
modelo.fit(X_train, y_train)
print("Coeficientes:")
print(pd.Series(modelo.coef_, index=X.columns).round(3))
print("Intercepto:", round(modelo.intercept_, 3))
print()

pred = modelo.predict(X_test)

# ---------------------------------------------------------------------------
# 4. Evaluar en datos que el modelo no vio
# ---------------------------------------------------------------------------
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)
print(f"MAE  = {mae:.2f}  -> en promedio el modelo se equivoca en {mae:.2f} puntos")
print(f"RMSE = {rmse:.2f}  -> como el MAE, pero castiga mas los errores grandes")
print(f"R2   = {r2:.2f}  (en datos de prueba)")
print()

# Linea base: predecir siempre el promedio. Un modelo util debe ganarle.
base = np.full(len(y_test), y_train.mean())
print(f"MAE de la linea base (predecir el promedio): {mean_absolute_error(y_test, base):.2f}")
print()

resultado = pd.DataFrame({"real": y_test.values, "predicha": pred.round(1)})
resultado["error"] = (resultado["real"] - resultado["predicha"]).round(1)
print("Primeras predicciones en datos de prueba:")
print(resultado.head(8))
