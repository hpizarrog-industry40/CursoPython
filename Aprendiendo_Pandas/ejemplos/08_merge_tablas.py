# 08 - Combinar tablas con merge()
#
# Objetivo: unir la base principal (alumnos) con una tabla auxiliar
# (cursos) usando una columna clave, y entender los tipos de join.
#
# Conceptos clave:
#   - Clave: columna que existe en ambas tablas y permite emparejar filas.
#   - Tabla principal: una fila por alumno (20 filas).
#   - Tabla auxiliar: una fila por curso (4 filas, incluye "Biologia",
#     un curso sin alumnos inscritos).

import pandas as pd

alumnos = pd.read_csv("datos/alumnos.csv")
cursos = pd.read_csv("datos/cursos.csv")

print("Tabla auxiliar de cursos:")
print(cursos)
print()

# ---------------------------------------------------------------------------
# 1. merge basico: agregar profesor, sala y creditos a cada alumno
# ---------------------------------------------------------------------------
# how="left" conserva TODAS las filas de la tabla de la izquierda (alumnos).
df = alumnos.merge(cursos, on="curso", how="left")
print("Alumnos con datos del curso (merge left):")
print(df[["nombre", "curso", "profesor", "sala"]].head())
print("Filas antes:", len(alumnos), "-> filas despues:", len(df))
print()

# ---------------------------------------------------------------------------
# 2. Tipos de join: inner, left, right, outer
# ---------------------------------------------------------------------------
# inner: solo claves presentes en AMBAS tablas
# left : todas las filas de la izquierda
# right: todas las filas de la derecha
# outer: todas las filas de ambas tablas
for tipo in ["inner", "left", "right", "outer"]:
    resultado = alumnos.merge(cursos, on="curso", how=tipo)
    print(f"how='{tipo}': {len(resultado)} filas")
print()

# ---------------------------------------------------------------------------
# 3. Trazabilidad: indicator=True agrega la columna _merge
# ---------------------------------------------------------------------------
# _merge dice de donde viene cada fila: both, left_only o right_only.
df_outer = alumnos.merge(cursos, on="curso", how="outer", indicator=True)
print("Origen de las filas (outer + indicator):")
print(df_outer["_merge"].value_counts())
print()
print("Filas que solo estan en la tabla de cursos:")
print(df_outer[df_outer["_merge"] == "right_only"][["curso", "profesor"]])
print()

# ---------------------------------------------------------------------------
# 4. Validar la relacion entre tablas
# ---------------------------------------------------------------------------
# validate="many_to_one" exige que la clave sea UNICA en la tabla derecha.
# Si cursos.csv tuviera un curso repetido, pandas lanzaria un MergeError
# en vez de duplicar alumnos en silencio.
df_validado = alumnos.merge(cursos, on="curso", how="left", validate="many_to_one")
print("merge validado (many_to_one) OK:", df_validado.shape)
print()

# ---------------------------------------------------------------------------
# 5. Cuando las claves tienen nombres distintos: left_on / right_on
# ---------------------------------------------------------------------------
cursos_renombrado = cursos.rename(columns={"curso": "nombre_curso"})
df_lr = alumnos.merge(cursos_renombrado, left_on="curso",
                      right_on="nombre_curso", how="left")
print("merge con left_on / right_on:", df_lr.shape)
