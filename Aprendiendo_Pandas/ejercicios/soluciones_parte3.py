# Soluciones de los ejercicios guiados - Parte 3 (uso del profesor)
#
#     cd ejercicios
#     python soluciones_parte3.py

import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("../datos/rendimiento.csv")


def ejercicio_1_correlacion(df):
    return round(df["asistencia"].corr(df["nota_final"]), 2)          # 0.61


def ejercicio_2_regresion_simple(df):
    modelo = smf.ols("nota_final ~ asistencia", data=df).fit()
    return {"intercepto": modelo.params["Intercept"],                  # -2.23
            "pendiente": modelo.params["asistencia"],                  # 0.096
            "r2": modelo.rsquared}                                     # 0.37


def ejercicio_3_predecir(df, asistencia):
    modelo = smf.ols("nota_final ~ asistencia", data=df).fit()
    nuevo = pd.DataFrame({"asistencia": [asistencia]})
    return float(modelo.predict(nuevo).iloc[0])                        # 90% -> 6.39


def ejercicio_4_regresion_multiple(df):
    datos = df.dropna(subset=["horas_sueno"])                          # 150 -> 146 filas
    formula = "nota_final ~ horas_estudio + asistencia + horas_sueno + C(trabaja)"
    return smf.ols(formula, data=datos).fit()


def ejercicio_5_variables_no_significativas(modelo):
    p = modelo.pvalues.drop("Intercept", errors="ignore")
    return p[p >= 0.05].index.tolist()                                 # ['horas_sueno']


if __name__ == "__main__":
    import ejercicios_parte3 as ej

    for nombre in ["ejercicio_1_correlacion", "ejercicio_2_regresion_simple",
                   "ejercicio_3_predecir", "ejercicio_4_regresion_multiple",
                   "ejercicio_5_variables_no_significativas"]:
        setattr(ej, nombre, globals()[nombre])

    for n, t in enumerate([ej.test_1, ej.test_2, ej.test_3, ej.test_4, ej.test_5], start=1):
        ej.comprobar(n, t)

    print()
    m = ejercicio_4_regresion_multiple(df)
    print("Modelo del ejercicio 4:")
    print(m.summary().tables[1])
    print()
    print("Reflexion para la clase: la asistencia sola explica el",
          f"{ejercicio_2_regresion_simple(df)['r2']:.0%} de la nota;",
          f"el modelo multiple llega a {m.rsquared_adj:.0%} (R2 ajustado).")
