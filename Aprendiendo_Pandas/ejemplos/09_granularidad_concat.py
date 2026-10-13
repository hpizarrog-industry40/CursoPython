# 09 - Granularidad y concatenacion de periodos
#
# Objetivo:
#   a) Detectar cuando dos tablas tienen distinta granularidad
#      (una fila por alumno vs. una fila por alumno y mes) y
#      ajustarla ANTES de hacer el merge.
#   b) Apilar dos periodos con pd.concat() sin perder la trazabilidad.

import pandas as pd

alumnos = pd.read_csv("datos/alumnos.csv")
asistencia = pd.read_csv("datos/asistencia_mensual.csv")

# ---------------------------------------------------------------------------
# PARTE A: granularidad
# ---------------------------------------------------------------------------
print("asistencia_mensual tiene", len(asistencia), "filas (3 meses x 20 alumnos)")
print(asistencia.head(6))
print()

# ERROR TIPICO: unir directamente tablas de distinta granularidad.
# Cada alumno aparece 3 veces -> la base principal se "infla".
malo = alumnos.merge(asistencia, on="id", how="left")
print("merge directo: de", len(alumnos), "a", len(malo), "filas  <-- se duplicaron alumnos")
print()

# validate="one_to_one" detecta el problema y lanza un error.
try:
    alumnos.merge(asistencia, on="id", validate="one_to_one")
except pd.errors.MergeError as e:
    print("validate detecto el problema:", e)
print()

# SOLUCION: llevar la tabla auxiliar a la MISMA granularidad (1 fila por id).
asistencia_alumno = (asistencia.groupby("id", as_index=False)["asistencia"]
                     .mean()
                     .rename(columns={"asistencia": "asistencia_mensual_prom"}))
bueno = alumnos.merge(asistencia_alumno, on="id", how="left", validate="one_to_one")
print("merge despues de agregar:", len(bueno), "filas")
print(bueno[["nombre", "asistencia", "asistencia_mensual_prom"]].head())
print()

# ---------------------------------------------------------------------------
# PARTE B: concatenar periodos
# ---------------------------------------------------------------------------
p1 = pd.read_csv("datos/alumnos.csv")
p2 = pd.read_csv("datos/alumnos_2026_2.csv")

# Antes de apilar: las columnas deben coincidir.
print("Mismas columnas en ambos periodos:", list(p1.columns) == list(p2.columns))

# Trazabilidad: agregar una columna que diga de que periodo viene cada fila.
p1["periodo"] = "2026-1"
p2["periodo"] = "2026-2"

historico = pd.concat([p1, p2], ignore_index=True)
print("Filas periodo 1:", len(p1), "| periodo 2:", len(p2), "| historico:", len(historico))
print(historico["periodo"].value_counts())
print()

# Ahora un mismo alumno puede aparecer dos veces: la clave pasa a ser (id, periodo).
print("Claves (id, periodo) duplicadas:", historico.duplicated(subset=["id", "periodo"]).sum())
print()

# Pregunta analitica: como cambio la nota final promedio por curso?
comparacion = historico.pivot_table(index="curso", columns="periodo",
                                    values="nota_final", aggfunc="mean").round(2)
print("Nota final promedio por curso y periodo:")
print(comparacion)
