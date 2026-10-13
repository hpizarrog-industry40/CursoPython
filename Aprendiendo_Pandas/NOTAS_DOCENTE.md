# Notas para el docente

Anotaciones por unidad: ideas clave, errores frecuentes de los estudiantes y
preguntas para verificar la comprensión, con la respuesta esperada según los
datos del curso.

---

## Unidad 1 — Introducción a Pandas

**Ideas clave**
- Un `DataFrame` es una tabla; cada columna es una `Series`.
- Antes de analizar, siempre: `shape`, `info()`, `describe()`, `isnull().sum()`.

**Errores frecuentes**
- Escribir `df.info` sin paréntesis: muestra el método, no la información.
- Confundir `describe()` (solo columnas numéricas por defecto) con un resumen de todas las columnas.

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Cuántas filas y columnas tiene `alumnos.csv`? | 20 filas, 9 columnas |
| ¿Qué columnas tienen faltantes? | `ciudad` (1), `nota_parcial1` (1), `nota_parcial2` (3) |
| ¿Cuál es la nota final promedio? | 6,98 |

---

## Unidad 2 — Filtrado, ordenamiento y selección

**Ideas clave**
- Una condición genera una *máscara* de `True`/`False`; `df[mascara]` deja las filas `True`.
- `loc` trabaja con etiquetas y `iloc` con posiciones.

**Errores frecuentes**
- Usar `and` / `or` en lugar de `&` / `|`.
- Olvidar los paréntesis: `df[df.a > 1 & df.b < 2]` falla por precedencia de operadores.
- Seleccionar varias columnas con un solo corchete: `df["a", "b"]`.

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Cuántos alumnos tienen nota final ≥ 8? | 5 |
| ¿Cuántos alumnos aprobaron (nota final ≥ 5)? | 17 |
| ¿Qué curso tiene mejor promedio? | Matemáticas (7,89) |
| ¿Quién tiene la mejor nota final? | Laura Martin (9,8) |

---

## Unidad 3 — Transformación y valores faltantes

**Ideas clave**
- Las operaciones con `NaN` devuelven `NaN`: el promedio de parciales queda vacío para 4 alumnos.
- Imputar no es neutral: con la media se reduce la variabilidad; con un valor fijo se marca el dato.
- Toda imputación o exclusión se documenta (celda de texto en Colab).

**Errores frecuentes**
- `df.fillna(0)` sin pensar: un 0 en una nota es un dato falso, no un faltante.
- `dropna()` sin mirar cuántas filas se pierden (aquí, 5 de 20 = 25 %).
- Olvidar asignar: `df["col"].fillna(x)` no modifica `df` si no se guarda el resultado.

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Con qué valor se imputa `nota_parcial2` si se usa la media? | 7,03 |
| ¿Cuántas filas quedan tras `dropna()`? | 15 |
| ¿Cuántos alumnos quedan en cada calificación? | Sobresaliente 3, Notable 8, Aprobado 6, Suspenso 3 |

---

## Unidad 4 — Combinación de tablas

**Ideas clave**
- **Clave:** la columna que empareja filas. Debe tener el mismo nombre y tipo en ambas tablas (o usar `left_on`/`right_on`).
- **Granularidad:** qué representa una fila. Antes de unir, ambas tablas deben estar al mismo nivel (por ejemplo, una fila por alumno).
- **Trazabilidad:** saber de dónde viene cada fila: `indicator=True`, una columna `periodo`, contar filas antes y después.
- `merge` agrega **columnas**; `concat` agrega **filas**.

**Errores frecuentes**
- Unir `asistencia_mensual.csv` directamente: la base pasa de 20 a 60 filas y los promedios quedan mal ponderados.
- Usar `how="inner"` sin darse cuenta de que se pierden filas.
- Apilar períodos sin una columna que los identifique (después no se puede comparar).

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Cuántas filas da `alumnos.merge(cursos, how=...)` con inner / left / right / outer? | 20 / 20 / 21 / 21 |
| ¿Qué curso aparece como `right_only`? | Biologia (sin alumnos) |
| ¿Cuántas filas da el merge directo con la asistencia mensual? | 60 (se triplica) |
| ¿Qué alumnos no continúan en 2026-2? | Diego Fernandez y Hugo Vega |
| ¿Cómo cambió la nota final promedio de Física entre períodos? | De 6,62 a 7,55 |

---

## Unidad 5 — Limpieza y automatización

**Ideas clave**
- Limpiar en un orden fijo: nombres de columnas → duplicados → texto → categorías → números → validación.
- `pd.to_numeric(..., errors="coerce")` convierte lo que no es número en `NaN` en vez de fallar.
- Una función por tarea, combinadas con `.pipe()`: el flujo se lee como una receta y se reutiliza.
- Cerrar siempre con validaciones (`assert`) y un registro de lo que se cambió.

**Errores frecuentes**
- Corregir a mano celda por celda (no es reproducible).
- Usar `str.title()` sin quitar las tildes: "Física" y "Fisica" siguen siendo dos categorías.
- Modificar el DataFrame original dentro de la función (usar `df = df.copy()`).

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Cuántas variantes de `curso` hay antes y después de limpiar? | 15 antes, 3 después |
| ¿Cuántas filas duplicadas tiene `alumnos_sucio.csv`? | 2 |
| ¿El resultado limpio coincide con `alumnos.csv`? | Sí: 20 filas y las mismas notas finales |

---

## Sugerencias para trabajar en Colab

- Pedir a los estudiantes **Archivo → Guardar una copia en Drive** antes de editar.
- Si un notebook “se rompe”, usar **Entorno de ejecución → Reiniciar y ejecutar todo**.
- Las soluciones están en una sección propia al final de cada notebook: se puede
  colapsar el título para que no se vean hasta la revisión.
