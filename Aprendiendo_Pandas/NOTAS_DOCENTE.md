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

## Unidad 6 — Uso estadístico: regresión lineal

**Ideas clave**
- Siempre graficar y calcular `r` antes de modelar: `r` solo detecta relaciones **lineales**.
- La pendiente se interpreta con unidades: “cada hora adicional de estudio se asocia con +0,40 puntos”.
- R² es la proporción de la variación explicada; para comparar modelos con distinto número de variables, usar **R² ajustado**.
- En la regresión múltiple cada coeficiente se lee “manteniendo constante el resto”.
- `statsmodels` sirve para **explicar** (p-valores, intervalos); `scikit-learn`, para **predecir y evaluar** con datos de prueba.

**Errores frecuentes**
- Decir que una variable “causa” la nota: los datos son observacionales; se dice “se asocia con”.
- Interpretar literalmente el intercepto (nota con 0 horas de estudio): es una extrapolación.
- Comparar modelos con R² simple (siempre sube al agregar variables).
- Olvidar `C()` en variables categóricas, o no saber cuál es la categoría de referencia (la primera en orden alfabético: Física; trabaja = No).
- Evaluar el modelo con los mismos datos con los que se entrenó.

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Qué variable se correlaciona más con la nota final? | `horas_estudio` (r = 0,80); asistencia 0,61; sueño −0,07 |
| ¿Cuál es la recta de la regresión simple con horas de estudio? | nota = 2,72 + 0,40 · horas, R² = 0,64 |
| ¿Qué nota predice para 7 horas de estudio? | 5,50 |
| ¿Por qué el coeficiente de horas de estudio baja de 0,40 a 0,31 en el modelo múltiple? | Parte del efecto se debía a asistir más y a no trabajar (variables relacionadas con estudiar) |
| ¿Qué variable no aporta al modelo múltiple? | `horas_sueno` (p = 0,65) |
| ¿Cuánto se equivoca en promedio el modelo con datos de prueba? | MAE = 0,70 puntos (predecir el promedio: 1,36) |
| Ejercicios guiados: recta con asistencia y predicción para 90 % | nota = −2,23 + 0,096 · asistencia, R² = 0,37; 6,39 |

---

## Unidad 7 — Modelos de predicción con árboles y forecasting

**Ideas clave**
- **Clasificación** predice una categoría (¿reprueba?); **regresión** predice un número. Los árboles hacen ambas.
- Un árbol aprende reglas *si … entonces …*; sin límite de profundidad **memoriza** (sobreajuste). `max_depth` lo controla.
- En una alerta temprana importa el **recall**: no avisar a quien reprobará es el error más caro.
- **Random Forest**: árboles en paralelo que votan. **XGBoost**: árboles en serie que corrigen el error anterior.
- Para interpretar, preferir la importancia **por permutación**: la de impureza favorece variables numéricas con muchos valores.
- En **forecasting** solo se usa información del pasado (`shift` dentro de `groupby("id")`) y la división es **por fecha**, nunca al azar.
- Siempre comparar contra una **línea base** (repetir la última nota) y contra un modelo simple.

**Errores frecuentes**
- Usar `train_test_split` al azar en una serie de tiempo: el modelo entrena con el futuro.
- Calcular rezagos sin `groupby("id")`: la semana 1 de un estudiante recibe la nota de otro.
- Usar variables de la misma semana que se pronostica (horas o asistencia de esa semana): es información que aún no existe.
- Concluir que una variable “no importa” porque su importancia es baja: puede estar correlacionada con otra.
- Suponer que el modelo más complejo siempre gana: en `rendimiento.csv` la regresión lineal le gana a Random Forest.

**Preguntas de verificación**
| Pregunta | Respuesta esperada |
|---|---|
| ¿Cuántos estudiantes reprueban? | 56 de 150 (37 %) |
| ¿Cuál es la primera pregunta del árbol de profundidad 3? | ¿horas_estudio ≤ 5,85? |
| Exactitud y recall del árbol de profundidad 3 | 0,87 y 0,88 (24 aciertos, 4 falsas alarmas, 2 no detectados, 15 detectados) |
| ¿Qué pasa con el árbol sin límite? | 100 % en entrenamiento y 0,80 en prueba: sobreajuste |
| Random Forest (200 árboles): exactitud y recall | 0,89 y 0,94 |
| ¿Qué variable sobrevalora la importancia por impureza? | `horas_sueno` (0,19 por impureza, ≈ 0 por permutación) |
| Alerta temprana con datos hasta la semana 6: recall de Random Forest | 0,94 (AUC 0,983) |
| MAE del pronóstico semanal (semanas 13-16) | XGBoost 0,63; ingenuo 0,74; regresión lineal 0,76 |
| ¿Qué variable de calendario mejora a todos los modelos? | `semanas_para_certamen` (XGBoost baja a 0,56) |

---

## Sugerencias para trabajar en Colab

- Pedir a los estudiantes **Archivo → Guardar una copia en Drive** antes de editar.
- Si un notebook “se rompe”, usar **Entorno de ejecución → Reiniciar y ejecutar todo**.
- Las soluciones están en una sección propia al final de cada notebook: se puede
  colapsar el título para que no se vean hasta la revisión.
- En la Parte 3, pedir que la interpretación de cada coeficiente se escriba en una
  celda de texto, con unidades y la frase “se asocia con”.
- En la Parte 4, conversar sobre el uso responsable de una alerta temprana: sirve para
  ofrecer apoyo, no para etiquetar a los estudiantes.
