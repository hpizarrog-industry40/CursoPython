# 14 - Regresion lineal multiple
#
# Objetivo: explicar la nota final con VARIAS variables a la vez,
# incluir variables categoricas, comparar modelos con R2 ajustado e
# identificar variables que no aportan.
#
# Requiere: pandas y statsmodels (vienen instalados en Google Colab).

import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("datos/rendimiento.csv")

# ---------------------------------------------------------------------------
# 1. Preparar los datos (lo aprendido en la Unidad 3)
# ---------------------------------------------------------------------------
# horas_sueno tiene 4 faltantes. Decision documentada: excluir esas filas
# (son menos del 3% de los datos y no hay una forma razonable de imputarlas).
print("Faltantes por columna:")
print(df.isnull().sum()[lambda s: s > 0])
datos = df.dropna(subset=["horas_sueno"])
print(f"Filas: {len(df)} -> {len(datos)} tras excluir faltantes en horas_sueno")
print()

# ---------------------------------------------------------------------------
# 2. Construir modelos de menos a mas variables
# ---------------------------------------------------------------------------
formulas = {
    "M1 simple":      "nota_final ~ horas_estudio",
    "M2 + asistencia": "nota_final ~ horas_estudio + asistencia",
    "M3 completo":    "nota_final ~ horas_estudio + asistencia + horas_sueno"
                      " + C(trabaja) + C(curso)",
}
modelos = {nombre: smf.ols(f, data=datos).fit() for nombre, f in formulas.items()}

comparacion = pd.DataFrame({
    "R2": [m.rsquared for m in modelos.values()],
    "R2_ajustado": [m.rsquared_adj for m in modelos.values()],
    "coef_horas_estudio": [m.params["horas_estudio"] for m in modelos.values()],
}, index=modelos.keys()).round(3)
print("Comparacion de modelos:")
print(comparacion)
print()
# R2 siempre sube al agregar variables; el R2 AJUSTADO penaliza las
# variables que no aportan, por eso es mejor para comparar modelos.

# (M1 usa 146 filas, por eso su coeficiente difiere levemente del ejemplo 13.)
# Observa que el efecto de horas_estudio BAJA del M1 al M3: en el modelo
# simple, horas_estudio tambien "absorbia" el efecto de asistir y de no
# trabajar. La regresion multiple separa esos efectos.

# ---------------------------------------------------------------------------
# 3. Leer la tabla de coeficientes del modelo completo
# ---------------------------------------------------------------------------
m3 = modelos["M3 completo"]
tabla = pd.DataFrame({
    "coeficiente": m3.params,
    "p_valor": m3.pvalues,
    "significativa": m3.pvalues < 0.05,
}).round(4)
print("Modelo completo:")
print(tabla)
print()

# Interpretacion ("manteniendo constante el resto de las variables"):
#   horas_estudio     : +1 hora semanal -> +0.31 puntos
#   asistencia        : +10 puntos de asistencia -> +0.39 puntos
#   C(trabaja)[T.Si]  : quienes trabajan obtienen ~0.86 puntos menos
#   C(curso)[T.Quimica]: Quimica ~0.44 puntos menos que Fisica
#                       (Fisica es la categoria de referencia: es la
#                        primera en orden alfabetico)
#   horas_sueno       : p = 0.65 -> no hay evidencia de que aporte
#   C(curso)[T.Matematicas]: p = 0.055, en el limite. Curso se mantiene en
#                       el modelo porque la diferencia de Quimica si es
#                       significativa: una variable categorica se decide
#                       completa, no categoria por categoria.

print("Variables NO significativas (p >= 0.05):",
      list(tabla.index[~tabla["significativa"]].drop("Intercept", errors="ignore")))
print()

# ---------------------------------------------------------------------------
# 4. Multicolinealidad: VIF (factor de inflacion de la varianza)
# ---------------------------------------------------------------------------
# Si dos predictores estan muy correlacionados, sus coeficientes se vuelven
# inestables. Regla practica: VIF > 5 merece atencion, VIF > 10 es grave.
X = m3.model.exog
vif = pd.Series([variance_inflation_factor(X, i) for i in range(X.shape[1])],
                index=m3.model.exog_names).drop("Intercept").round(2)
print("VIF por variable:")
print(vif)
print()

# ---------------------------------------------------------------------------
# 5. Modelo final: quitar lo que no aporta
# ---------------------------------------------------------------------------
final = smf.ols("nota_final ~ horas_estudio + asistencia + C(trabaja) + C(curso)",
                data=datos).fit()
print(f"Modelo final sin horas_sueno: R2 ajustado = {final.rsquared_adj:.3f} "
      f"(completo: {m3.rsquared_adj:.3f})")

estudiante = pd.DataFrame({"horas_estudio": [8], "asistencia": [90],
                           "trabaja": ["No"], "curso": ["Matematicas"]})
print("Prediccion para un estudiante de Matematicas que estudia 8 h,",
      "asiste 90% y no trabaja:", round(final.predict(estudiante).iloc[0], 2))
