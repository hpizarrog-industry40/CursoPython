# 17 - Random Forest: muchos arboles votando
#
# Objetivo: entender por que un "bosque" de arboles suele ser mas estable
# que un solo arbol, leer la importancia de las variables con cuidado y
# comparar honestamente con la regresion lineal de la unidad 6.
#
# Idea: cada arbol se entrena con una muestra al azar de estudiantes y,
# en cada pregunta, con un subconjunto al azar de variables. La prediccion
# final es el VOTO de todos los arboles (o el promedio, en regresion).
#
# Requiere: pandas, matplotlib y scikit-learn (vienen instalados en Colab).

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("datos/rendimiento.csv")
df["reprueba"] = (df["nota_final"] < 5).astype(int)
# Aqui SI incluimos horas_sueno, a proposito, para ver como la tratan las
# medidas de importancia. Sus 4 faltantes se imputan con la mediana.
df["horas_sueno"] = df["horas_sueno"].fillna(df["horas_sueno"].median())

X = pd.get_dummies(df[["horas_estudio", "asistencia", "horas_sueno", "trabaja", "curso"]],
                   columns=["trabaja", "curso"], drop_first=True, dtype=int)
y = df["reprueba"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# ---------------------------------------------------------------------------
# 1. Un arbol vs. un bosque
# ---------------------------------------------------------------------------
arbol = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)   # sin limite
bosque = RandomForestClassifier(n_estimators=300, random_state=42).fit(X_train, y_train)

for nombre, modelo in [("Arbol sin limite", arbol), ("Random Forest (300)", bosque)]:
    p = modelo.predict(X_test)
    print(f"{nombre:<20} exactitud = {accuracy_score(y_test, p):.2f}   "
          f"recall reprobados = {recall_score(y_test, p):.2f}")
print()
# El bosque corrige buena parte del sobreajuste del arbol individual sin
# tener que elegir a mano la profundidad.

# ---------------------------------------------------------------------------
# 2. Importancia de variables: dos formas de medirla
# ---------------------------------------------------------------------------
imp = pd.DataFrame({
    # a) Impureza: rapida, pero favorece variables numericas con muchos valores
    "impureza": bosque.feature_importances_,
    # b) Permutacion: desordena una variable y mide cuanto empeora el modelo
    "permutacion": permutation_importance(bosque, X_test, y_test, n_repeats=30,
                                          random_state=42).importances_mean,
}, index=X.columns).round(3).sort_values("permutacion", ascending=False)
print("Importancia de variables:")
print(imp)
print()
# Observa horas_sueno: la importancia por impureza le da peso, pero la de
# permutacion es casi cero. En la unidad 6 vimos que NO aporta (p = 0.65).
# Conclusion: preferir la importancia por permutacion para interpretar.
# Ojo con asistencia: tambien queda baja porque esta correlacionada con
# horas_estudio (r = 0.62); el bosque obtiene casi la misma informacion de
# cualquiera de las dos. Importancia baja != variable irrelevante.

imp["permutacion"].sort_values().plot(kind="barh", title="Importancia por permutacion")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 3. Comparacion honesta: Random Forest vs. regresion lineal (nota_final)
# ---------------------------------------------------------------------------
Xr = X.drop(columns=["horas_sueno"])
yr = df["nota_final"]
Xr_train, Xr_test, yr_train, yr_test = train_test_split(Xr, yr, test_size=0.2, random_state=42)

lineal = LinearRegression().fit(Xr_train, yr_train)
rf_reg = RandomForestRegressor(n_estimators=300, min_samples_leaf=3,
                               random_state=42).fit(Xr_train, yr_train)
print("Prediccion de nota_final (MAE en datos de prueba):")
print(f"  Regresion lineal: {mean_absolute_error(yr_test, lineal.predict(Xr_test)):.2f}")
print(f"  Random Forest   : {mean_absolute_error(yr_test, rf_reg.predict(Xr_test)):.2f}")
# Cuando la relacion real es LINEAL (como aqui), la regresion lineal gana:
# es mas simple y aprovecha mejor pocos datos. Los arboles brillan cuando
# hay umbrales, interacciones y relaciones no lineales (ejemplo 19).
