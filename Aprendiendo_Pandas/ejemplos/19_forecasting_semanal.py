# 19 - Forecasting: pronosticar la nota del proximo control semanal
#
# Pregunta: con lo que sabemos HASTA la semana anterior, ¿que nota sacara
# cada estudiante en el control de la proxima semana?
#
# Conceptos de series de tiempo:
#   - Rezagos (lags): el valor de semanas anteriores como variable explicativa.
#   - Medias moviles: promedio de las ultimas k semanas.
#   - Variables de calendario: semana de certamen (8 y 16).
#   - Division TEMPORAL: se entrena con el pasado y se prueba con el futuro.
#     ¡Nunca mezclar al azar semanas futuras en el entrenamiento!
#
# Requiere: pandas, matplotlib, scikit-learn y xgboost (instalados en Colab).

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor

semanal = pd.read_csv("datos/seguimiento_semanal.csv", parse_dates=["fecha"])
final = pd.read_csv("datos/rendimiento.csv")
df = semanal.merge(final[["id", "trabaja"]], on="id", how="left", validate="many_to_one")
df = df.sort_values(["id", "semana"]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 1. Mirar la serie: promedio semanal por grupo
# ---------------------------------------------------------------------------
por_semana = df.pivot_table(index="semana", columns="trabaja",
                            values=["asistencia", "nota_control"], aggfunc="mean").round(2)
print("Promedios por semana (No trabaja / Si trabaja):")
print(por_semana)
print()
# Patrones: la asistencia de quienes trabajan cae desde la semana 7, y en las
# semanas de certamen (8 y 16) las notas se separan entre ambos grupos.

fig, (e1, e2) = plt.subplots(1, 2, figsize=(13, 4))
por_semana["asistencia"].plot(ax=e1, marker="o", title="Asistencia promedio por semana")
por_semana["nota_control"].plot(ax=e2, marker="o", title="Nota de control promedio por semana")
for eje in (e1, e2):
    for s in (8, 16):
        eje.axvline(s, color="gray", linestyle="--", linewidth=1)
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 2. Construir variables con informacion del PASADO (por estudiante)
# ---------------------------------------------------------------------------
g = df.groupby("id")
df["nota_lag1"] = g["nota_control"].shift(1)          # nota de la semana anterior
df["nota_lag2"] = g["nota_control"].shift(2)          # nota de hace dos semanas
df["nota_media3"] = g["nota_control"].transform(lambda s: s.shift(1).rolling(3).mean())
df["nota_media_acum"] = g["nota_control"].transform(lambda s: s.shift(1).expanding().mean())
df["asistencia_lag1"] = g["asistencia"].shift(1)
df["horas_lag1"] = g["horas_estudio"].shift(1)
df["es_certamen"] = df["semana"].isin([8, 16]).astype(int)   # calendario: se conoce de antemano
# Semanas que faltan para el proximo certamen (8 o 16): tambien es calendario
df["semanas_para_certamen"] = df["semana"].apply(lambda s: 8 - s if s <= 8 else 16 - s)
df["trabaja_si"] = (df["trabaja"] == "Si").astype(int)

VARIABLES = ["semana", "es_certamen", "trabaja_si", "nota_lag1", "nota_lag2",
             "nota_media3", "nota_media_acum", "asistencia_lag1", "horas_lag1"]
print(df[["id", "semana", "nota_control", "nota_lag1", "nota_lag2", "nota_media3"]].head(6))
print()

# Las primeras 3 semanas no tienen historia suficiente: se excluyen.
modelo_df = df.dropna(subset=VARIABLES)
# Variante mejorada (seccion 6): cambiar "semana" por "semanas_para_certamen"
VARIABLES_CAL = ["semanas_para_certamen"] + VARIABLES[1:]

# ---------------------------------------------------------------------------
# 3. Division temporal: semanas 4-12 para entrenar, 13-16 para probar
# ---------------------------------------------------------------------------
train = modelo_df[modelo_df["semana"] <= 12]
test = modelo_df[modelo_df["semana"] >= 13]
print(f"Entrenamiento: semanas 4-12 ({len(train)} filas) | Prueba: semanas 13-16 ({len(test)} filas)")
print()

# ---------------------------------------------------------------------------
# 4. Lineas base: todo modelo debe ganarles
# ---------------------------------------------------------------------------
resultados = {
    "Ingenuo (repetir la ultima nota)": test["nota_lag1"],
    "Media de las ultimas 3 semanas": test["nota_media3"],
}

# ---------------------------------------------------------------------------
# 5. Modelos
# ---------------------------------------------------------------------------
modelos = {
    "Regresion lineal": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.05, random_state=42),
}
for nombre, modelo in modelos.items():
    modelo.fit(train[VARIABLES], train["nota_control"])
    resultados[nombre] = pd.Series(modelo.predict(test[VARIABLES]), index=test.index)

certamen = test["es_certamen"] == 1
tabla = pd.DataFrame({
    "MAE_total": {n: mean_absolute_error(test["nota_control"], p) for n, p in resultados.items()},
    "MAE_certamen": {n: mean_absolute_error(test.loc[certamen, "nota_control"], p[certamen])
                     for n, p in resultados.items()},
}).round(3).sort_values("MAE_total")
print("Error medio absoluto en las semanas 13-16 (menor es mejor):")
print(tabla)
print()
# XGBoost gana porque descubre solo las INTERACCIONES (trabajar x semana de
# certamen) y los UMBRALES (asistencia baja -> nota baja la semana siguiente)
# que la regresion lineal no puede representar sin ayuda.

importancia = pd.Series(modelos["XGBoost"].feature_importances_, index=VARIABLES)
print("Importancia en XGBoost (version con 'semana'):")
print(importancia.sort_values(ascending=False).round(3))
print()

# ---------------------------------------------------------------------------
# 6. Mejorar las VARIABLES antes que el algoritmo
# ---------------------------------------------------------------------------
# Antes de un certamen los estudiantes estudian mas y suben sus notas. La
# variable "semana" no lo expresa bien; "semanas_para_certamen" si.
mejora = {}
for nombre, modelo in modelos.items():
    modelo.fit(train[VARIABLES_CAL], train["nota_control"])
    pred = pd.Series(modelo.predict(test[VARIABLES_CAL]), index=test.index)
    mejora[nombre] = {"MAE_con_semana": tabla.loc[nombre, "MAE_total"],
                      "MAE_con_calendario": round(mean_absolute_error(test["nota_control"], pred), 3)}
    resultados[nombre + " + calendario"] = pred
print("Efecto de una mejor variable de calendario:")
print(pd.DataFrame(mejora).T)
print()
# La regresion lineal mejora mas con la nueva variable que cambiando de
# algoritmo: una buena variable vale mas que un modelo mas complejo.

# ---------------------------------------------------------------------------
# 7. Pronostico del certamen final (semana 16) y vista del curso
# ---------------------------------------------------------------------------
# clip(1, 10): las notas van de 1 a 10, el modelo podria salirse levemente del rango
test = test.assign(pronostico=resultados["XGBoost + calendario"].clip(1, 10).round(1))
sem16 = test[test["semana"] == 16][["id", "trabaja", "nota_lag1", "pronostico", "nota_control"]]
print("Pronostico del certamen final (primeros 8 estudiantes):")
print(sem16.head(8).to_string(index=False))
print()

curso = test.groupby("semana")[["nota_control", "pronostico"]].mean().round(2)
print("Promedio del curso: real vs. pronostico XGBoost + calendario")
print(curso)
curso.plot(marker="o", title="Nota de control promedio: real vs. pronostico")
plt.show()
