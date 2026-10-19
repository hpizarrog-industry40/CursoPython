# 16 - Arbol de decision: clasificar quien reprobara
#
# Objetivo: pasar de PREDECIR UN NUMERO (regresion, unidad 6) a PREDECIR
# UNA CATEGORIA (clasificacion): ¿el estudiante reprobara? (nota_final < 5).
# Un arbol de decision aprende reglas del tipo "si ... entonces ...",
# faciles de leer y explicar.
#
# Datos: datos/rendimiento.csv (los mismos 150 estudiantes de la unidad 6)
# Requiere: pandas, matplotlib y scikit-learn (vienen instalados en Colab).

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

df = pd.read_csv("datos/rendimiento.csv")

# ---------------------------------------------------------------------------
# 1. Variable objetivo (y): 1 = reprueba, 0 = aprueba
# ---------------------------------------------------------------------------
df["reprueba"] = (df["nota_final"] < 5).astype(int)
print("Estudiantes que reprueban:", df["reprueba"].sum(), "de", len(df),
      f"({df['reprueba'].mean():.0%})")
print()

# ---------------------------------------------------------------------------
# 2. Variables explicativas (X)
# ---------------------------------------------------------------------------
# Decision documentada: se excluye horas_sueno porque en la unidad 6 vimos
# que no aporta (p = 0.65). Un arbol tambien puede "aprender" ruido: con
# pocas filas, cortaria en horas_sueno por casualidad (ver ejemplo 17).
X = pd.get_dummies(df[["horas_estudio", "asistencia", "trabaja", "curso"]],
                   columns=["trabaja", "curso"], drop_first=True, dtype=int)
y = df["reprueba"]

# stratify=y mantiene la misma proporcion de reprobados en ambos conjuntos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)
print(f"Entrenamiento: {len(X_train)} | Prueba: {len(X_test)}")
print()

# ---------------------------------------------------------------------------
# 3. Entrenar un arbol pequeno (max_depth=3: a lo mas 3 preguntas seguidas)
# ---------------------------------------------------------------------------
arbol = DecisionTreeClassifier(max_depth=3, random_state=42)
arbol.fit(X_train, y_train)

print("Reglas aprendidas por el arbol:")
print(export_text(arbol, feature_names=list(X.columns)))

# ---------------------------------------------------------------------------
# 4. Evaluar con datos de prueba
# ---------------------------------------------------------------------------
pred = arbol.predict(X_test)
print(f"Exactitud (accuracy): {accuracy_score(y_test, pred):.2f}")
# Recall de la clase 1: de los que realmente reprueban, ¿a cuantos detecta?
print(f"Recall (reprobados detectados): {recall_score(y_test, pred):.2f}")
print()
print("Matriz de confusion (filas = real, columnas = predicho):")
print(pd.DataFrame(confusion_matrix(y_test, pred),
                   index=["real aprueba", "real reprueba"],
                   columns=["pred aprueba", "pred reprueba"]))
print()

# ---------------------------------------------------------------------------
# 5. Sobreajuste: ¿que pasa si dejamos crecer el arbol sin limite?
# ---------------------------------------------------------------------------
print("Profundidad | exactitud entrenamiento | exactitud prueba")
for profundidad in [1, 2, 3, 4, 6, None]:
    a = DecisionTreeClassifier(max_depth=profundidad, random_state=42).fit(X_train, y_train)
    print(f"{str(profundidad):>11} | {accuracy_score(y_train, a.predict(X_train)):>23.2f} |"
          f" {accuracy_score(y_test, a.predict(X_test)):>16.2f}")
# Sin limite, el arbol MEMORIZA el entrenamiento (100%) pero empeora en
# datos nuevos: eso es sobreajuste (overfitting). Profundidad 3 es el mejor
# equilibrio en estos datos.
print()

# ---------------------------------------------------------------------------
# 6. Probabilidad de reprobar para un estudiante nuevo
# ---------------------------------------------------------------------------
nuevo = pd.DataFrame([{c: 0 for c in X.columns}])
nuevo[["horas_estudio", "asistencia", "trabaja_Si"]] = [4, 70, 1]
print("Estudiante que estudia 4 h, asiste 70% y trabaja:")
print(f"  probabilidad de reprobar = {arbol.predict_proba(nuevo)[0, 1]:.0%}")

# ---------------------------------------------------------------------------
# 7. Dibujar el arbol
# ---------------------------------------------------------------------------
plt.figure(figsize=(16, 7))
plot_tree(arbol, feature_names=list(X.columns), class_names=["aprueba", "reprueba"],
          filled=True, rounded=True, fontsize=9)
plt.title("Arbol de decision (max_depth=3)")
plt.show()
