# 13 - Regresion lineal simple
#
# Objetivo: ajustar la recta  nota_final = b0 + b1 * horas_estudio,
# interpretar sus coeficientes, medir el ajuste (R2) y hacer predicciones.
#
# Requiere: pandas, matplotlib y statsmodels (vienen instalados en Google Colab).
# En local:  pip install statsmodels matplotlib

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("datos/rendimiento.csv")

# ---------------------------------------------------------------------------
# 1. Ajustar el modelo con una formula:  "y ~ x"
# ---------------------------------------------------------------------------
modelo = smf.ols("nota_final ~ horas_estudio", data=df).fit()

b0 = modelo.params["Intercept"]       # intercepto
b1 = modelo.params["horas_estudio"]   # pendiente
print(f"Recta ajustada: nota_final = {b0:.2f} + {b1:.3f} * horas_estudio")
print()

# ---------------------------------------------------------------------------
# 2. Interpretacion
# ---------------------------------------------------------------------------
print(f"Pendiente: por cada hora extra de estudio semanal, la nota final")
print(f"           aumenta en promedio {b1:.2f} puntos.")
print(f"Intercepto: nota esperada con 0 horas de estudio = {b0:.2f}")
print("            (es una extrapolacion: casi nadie estudia 0 horas).")
print()
print(f"R2 = {modelo.rsquared:.3f} -> las horas de estudio explican el "
      f"{modelo.rsquared:.0%} de la variacion de la nota final.")
print(f"p-valor de la pendiente = {modelo.pvalues['horas_estudio']:.2e} "
      "(< 0.05: la relacion es estadisticamente significativa)")
print()

# Resumen completo de statsmodels (tabla de coeficientes, R2, etc.)
print(modelo.summary())
print()

# ---------------------------------------------------------------------------
# 3. Comprobacion "a mano": b1 = cov(x, y) / var(x)
# ---------------------------------------------------------------------------
x, y = df["horas_estudio"], df["nota_final"]
b1_manual = x.cov(y) / x.var()
b0_manual = y.mean() - b1_manual * x.mean()
print(f"Calculo manual: b0 = {b0_manual:.3f}, b1 = {b1_manual:.3f}  (igual que statsmodels)")
print()

# ---------------------------------------------------------------------------
# 4. Predicciones
# ---------------------------------------------------------------------------
nuevos = pd.DataFrame({"horas_estudio": [3, 7, 12]})
nuevos["nota_predicha"] = modelo.predict(nuevos).round(2)
print("Predicciones:")
print(nuevos)
print()

# ---------------------------------------------------------------------------
# 5. Residuos: lo que el modelo NO explica
# ---------------------------------------------------------------------------
df["prediccion"] = modelo.fittedvalues
df["residuo"] = modelo.resid       # residuo = real - predicho
print("Promedio de los residuos (debe ser ~0):", round(df["residuo"].mean(), 6))
print()

fig, (eje1, eje2) = plt.subplots(1, 2, figsize=(12, 4))
eje1.scatter(x, y, alpha=0.6, label="datos")
orden = x.sort_values()
eje1.plot(orden, b0 + b1 * orden, color="red", label="recta ajustada")
eje1.set_xlabel("horas_estudio")
eje1.set_ylabel("nota_final")
eje1.legend()
eje1.set_title(f"R2 = {modelo.rsquared:.2f}")

# Si el modelo es adecuado, los residuos se ven como una nube sin patron
eje2.scatter(df["prediccion"], df["residuo"], alpha=0.6)
eje2.axhline(0, color="red")
eje2.set_xlabel("nota predicha")
eje2.set_ylabel("residuo")
eje2.set_title("Residuos vs. predichos")
plt.tight_layout()
plt.show()
