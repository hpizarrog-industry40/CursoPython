# 12 - Correlacion y diagramas de dispersion
#
# Objetivo: antes de construir un modelo, explorar la relacion entre
# variables numericas con graficos de dispersion y el coeficiente de
# correlacion de Pearson (r).
#
# Datos: datos/rendimiento.csv (150 estudiantes)
#   horas_estudio : horas de estudio semanales
#   asistencia    : porcentaje de asistencia
#   horas_sueno   : horas de sueno promedio por noche (4 valores faltantes)
#   trabaja       : "Si" / "No"
#   curso         : Matematicas, Fisica o Quimica
#   nota_final    : nota final (1-10)  <-- variable a explicar
#
# Requiere: pandas y matplotlib (ambos vienen instalados en Google Colab)

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("datos/rendimiento.csv")
print(df.head())
print()
df.info()
print()

# ---------------------------------------------------------------------------
# 1. Matriz de correlacion
# ---------------------------------------------------------------------------
# r va de -1 a 1:
#   cerca de  1 -> relacion lineal positiva fuerte
#   cerca de  0 -> sin relacion LINEAL
#   cerca de -1 -> relacion lineal negativa fuerte
numericas = ["horas_estudio", "asistencia", "horas_sueno", "nota_final"]
matriz = df[numericas].corr().round(2)
print("Matriz de correlacion:")
print(matriz)
print()

# Correlacion de cada variable con la nota final, ordenada
print("Correlacion con nota_final:")
print(matriz["nota_final"].drop("nota_final").sort_values(ascending=False))
print()


def interpretar_r(r):
    """Escala orientativa para interpretar el valor absoluto de r."""
    a = abs(r)
    if a >= 0.7:
        fuerza = "fuerte"
    elif a >= 0.4:
        fuerza = "moderada"
    elif a >= 0.2:
        fuerza = "debil"
    else:
        fuerza = "muy debil o nula"
    signo = "positiva" if r > 0 else "negativa"
    return f"r = {r:.2f}: relacion {fuerza} {signo}"


for col in ["horas_estudio", "asistencia", "horas_sueno"]:
    print(f"{col:<14}", interpretar_r(df[col].corr(df["nota_final"])))
print()

# ---------------------------------------------------------------------------
# 2. Ojo: las variables explicativas tambien se relacionan entre si
# ---------------------------------------------------------------------------
# horas_estudio y asistencia tienen r = 0.62: quien estudia mas tambien
# suele asistir mas. Esto importa en la regresion multiple (ejemplo 14).
print("horas_estudio vs asistencia:",
      interpretar_r(df["horas_estudio"].corr(df["asistencia"])))
print()

# ---------------------------------------------------------------------------
# 3. Graficos de dispersion
# ---------------------------------------------------------------------------
fig, ejes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
for eje, col in zip(ejes, ["horas_estudio", "asistencia", "horas_sueno"]):
    eje.scatter(df[col], df["nota_final"], alpha=0.6)
    eje.set_xlabel(col)
    eje.set_title(f"r = {df[col].corr(df['nota_final']):.2f}")
ejes[0].set_ylabel("nota_final")
plt.suptitle("Nota final vs. posibles variables explicativas")
plt.tight_layout()
plt.show()

# Recordatorio: correlacion NO implica causalidad. Un r alto dice que dos
# variables se mueven juntas, no que una cause a la otra.
