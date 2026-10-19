# 18 - XGBoost: sistema de alerta temprana
#
# Pregunta: con lo que sabemos en la SEMANA 6 del semestre, ¿podemos
# anticipar que estudiantes reprobaran el curso?
#
# Usa todo lo aprendido: groupby para cambiar la granularidad (unidad 4),
# merge con validacion, variables derivadas, y compara cuatro modelos.
#
# XGBoost (eXtreme Gradient Boosting) construye arboles EN SERIE: cada arbol
# nuevo se concentra en corregir los errores de los anteriores.
#
# Datos: datos/seguimiento_semanal.csv (150 estudiantes x 16 semanas)
#        datos/rendimiento.csv          (resultado final del curso)
# Requiere: pandas, scikit-learn y xgboost (vienen instalados en Colab).
# En local:  pip install xgboost

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

semanal = pd.read_csv("datos/seguimiento_semanal.csv")
final = pd.read_csv("datos/rendimiento.csv")
print("seguimiento_semanal:", semanal.shape, "-> 1 fila por estudiante y semana")
print(semanal.head())
print()

# ---------------------------------------------------------------------------
# 1. Resumir las semanas 1 a 6 (cambiar la granularidad a 1 fila por id)
# ---------------------------------------------------------------------------
primeras = semanal[semanal["semana"] <= 6]
resumen = primeras.groupby("id", as_index=False).agg(
    asistencia_prom=("asistencia", "mean"),
    horas_prom=("horas_estudio", "mean"),
    entregas=("entrega_tarea", "sum"),
    nota_control_prom=("nota_control", "mean"),
)
# Tendencia: asistencia de las semanas 4-6 menos la de las semanas 1-3
s13 = primeras[primeras["semana"] <= 3].groupby("id")["asistencia"].mean()
s46 = primeras[primeras["semana"] >= 4].groupby("id")["asistencia"].mean()
resumen["tendencia_asistencia"] = (s46 - s13).values

# ---------------------------------------------------------------------------
# 2. Unir con el resultado final (la variable a predecir)
# ---------------------------------------------------------------------------
final["reprueba"] = (final["nota_final"] < 5).astype(int)
datos = resumen.merge(final[["id", "trabaja", "curso", "reprueba"]],
                      on="id", how="left", validate="one_to_one")
print("Tabla para el modelo:", datos.shape)
print(datos.head())
print()

X = pd.get_dummies(datos.drop(columns=["id", "reprueba"]),
                   columns=["trabaja", "curso"], drop_first=True, dtype=int)
y = datos["reprueba"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# ---------------------------------------------------------------------------
# 3. Comparar cuatro modelos
# ---------------------------------------------------------------------------
modelos = {
    "Regresion logistica": LogisticRegression(max_iter=1000),
    "Arbol (prof. 3)": DecisionTreeClassifier(max_depth=3, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=300, random_state=42),
    "XGBoost": XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.1,
                             random_state=42),
}
filas = []
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)
    prob = modelo.predict_proba(X_test)[:, 1]
    filas.append({"modelo": nombre,
                  "exactitud": accuracy_score(y_test, pred),
                  "recall": recall_score(y_test, pred),
                  "AUC": roc_auc_score(y_test, prob)})
comparacion = pd.DataFrame(filas).set_index("modelo").round(3)
print("Comparacion (datos de prueba):")
print(comparacion)
print()
# recall: de los que realmente reprueban, ¿que proporcion detecta la alerta?
# AUC: capacidad de ordenar del mas al menos riesgoso (1 = perfecto, 0.5 = azar)

# ---------------------------------------------------------------------------
# 4. Hiperparametros principales de XGBoost
# ---------------------------------------------------------------------------
#   n_estimators : cuantos arboles en serie
#   max_depth    : profundidad de cada arbol (arboles pequenos = menos sobreajuste)
#   learning_rate: cuanto corrige cada arbol (pequeno = aprende lento pero seguro)
print("Efecto de learning_rate (con 200 arboles):")
for lr in [0.01, 0.1, 0.5]:
    m = XGBClassifier(n_estimators=200, max_depth=3, learning_rate=lr,
                      random_state=42).fit(X_train, y_train)
    print(f"  learning_rate={lr:<5} AUC prueba = "
          f"{roc_auc_score(y_test, m.predict_proba(X_test)[:, 1]):.3f}")
print()

# ---------------------------------------------------------------------------
# 5. La alerta: lista de estudiantes de prueba ordenados por riesgo
# ---------------------------------------------------------------------------
xgb = modelos["XGBoost"]
alerta = datos.loc[X_test.index, ["id", "asistencia_prom", "nota_control_prom", "reprueba"]].copy()
alerta["prob_reprobar"] = xgb.predict_proba(X_test)[:, 1].round(2)
alerta = alerta.sort_values("prob_reprobar", ascending=False)
print("Top 10 estudiantes con mayor riesgo (semana 6):")
print(alerta.head(10).to_string(index=False))
print()

importancia = pd.Series(xgb.feature_importances_, index=X.columns).sort_values(ascending=False)
print("Variables mas usadas por XGBoost:")
print(importancia.round(3))
