# Programa de estudio — Programación en Python: análisis de datos con Pandas

| | |
|---|---|
| **Asignatura** | Programación en Python |
| **Módulo** | Manipulación y preparación de datos con Pandas (Solemne 1) |
| **Herramienta de trabajo** | Google Colab (navegador + cuenta Google, sin instalación) |
| **Material** | Este repositorio: `datos/`, `ejemplos/`, `ejercicios/`, `notebooks/` |
| **Requisito previo** | Python básico: variables, listas, diccionarios, funciones, `if` y `for` |

## Resultado de aprendizaje general

Al terminar el módulo, el estudiante prepara una base de datos real para el análisis:
la carga y explora, filtra y ordena según una pregunta, crea variables derivadas,
trata los datos faltantes de forma justificada, integra varias tablas sin perder
trazabilidad y automatiza la limpieza con funciones reutilizables.

## Unidades

| # | Unidad | Objetivo de aprendizaje | Contenidos | Material | Evidencia |
|---|---|---|---|---|---|
| 1 | Introducción a Pandas: DataFrames, carga de datos y exploración inicial | Usar DataFrames para describir y explorar bases de datos | `read_csv`, `head`, `tail`, `shape`, `info`, `describe`, `dtypes`, `value_counts`, selección de columnas, primeras validaciones | `01_lectura_csv.py`, `02_exploracion_datos.py` | Ejercicio 4 (parte 1) |
| 2 | Filtrado, ordenamiento, selección y transformación | Filtrar observaciones relevantes y ordenar datos según preguntas analíticas | `loc`, `iloc`, máscaras booleanas, `&`, `\|`, `isin`, `sort_values`, `groupby` + `mean` | `03_seleccion_filtrado.py`, `05_agrupacion.py`, `07_ordenar_exportar.py` | Ejercicios 1, 2 y 3 (parte 1) |
| 3 | Transformación de datos y tratamiento de valores faltantes | Crear variables derivadas y tratar datos faltantes de forma documentada | Columnas calculadas, `apply`, `rename`, `drop`, `isnull`, `fillna`, `dropna`, registro de decisiones | `04_operaciones_columnas.py`, `06_valores_faltantes.py` | Ejercicio 5 (parte 1) + registro de decisiones |
| 4 | Combinación de tablas: joins, merges y concatenaciones | Integrar varias tablas respetando claves, granularidad y trazabilidad | `merge` (`on`, `how`, `left_on/right_on`), tipos de join, `indicator`, `validate`, granularidad, `groupby` antes de unir, `concat`, columna de período, `pivot_table` | `08_merge_tablas.py`, `09_granularidad_concat.py` | Ejercicios 1 a 4 (parte 2) |
| 5 | Limpieza de datos reales y automatización simple de tareas rutinarias | Diseñar un flujo reutilizable de limpieza y preparación de datos | Nombres de columnas, `drop_duplicates`, métodos `.str`, quitar tildes, mapeo de categorías, `to_numeric(errors="coerce")`, funciones, `.pipe()`, registro de limpieza, `assert` | `10_limpieza_datos.py`, `11_funcion_limpieza.py` | Ejercicio 5 (parte 2) |
| 6 | Uso estadístico con Python *(próximo módulo)* | Regresión lineal simple y múltiple | Ejercicios guiados | *Pendiente* | — |

## Planificación sugerida de sesiones

Las duraciones son orientativas; ajústelas al horario real del curso.

| Sesión | Contenido | Notebook | Actividad |
|---|---|---|---|
| 1 | Presentación de Colab + Unidad 1 | `notebooks/Parte1_Pandas_Colab.ipynb` (secciones 0 y 1) | Explorar `alumnos.csv` y responder: ¿cuántas filas, qué tipos, cuántos faltantes? |
| 2 | Unidades 2 y 3 | Parte 1 (secciones 2 y 3) | Filtrar, ordenar, crear `calificacion` y completar el registro de decisiones |
| 3 | Práctica parte 1 | Parte 1 (ejercicios y soluciones) | Ejercicios 1–5 y revisión colectiva de las soluciones |
| 4 | Unidad 4 | `notebooks/Parte2_Pandas_Colab.ipynb` (sección 4) | Unir alumnos y cursos, detectar el problema de granularidad y apilar períodos |
| 5 | Unidad 5 | Parte 2 (sección 5) | Limpiar `alumnos_sucio.csv` paso a paso y convertirlo en una función |
| 6 | Práctica parte 2 | Parte 2 (ejercicios y soluciones) | Ejercicios 1–5 con comprobación automática |

## Datos del curso

| Archivo | Filas | Granularidad | Uso |
|---|---|---|---|
| `datos/alumnos.csv` | 20 | 1 fila por alumno | Base principal (unidades 1–4) |
| `datos/cursos.csv` | 4 | 1 fila por curso | Tabla auxiliar para `merge` (incluye *Biologia*, sin alumnos) |
| `datos/asistencia_mensual.csv` | 60 | 1 fila por alumno y mes | Ejemplo de granularidad distinta |
| `datos/alumnos_2026_2.csv` | 20 | 1 fila por alumno | Segundo período para `concat` (2 alumnos salen, 2 entran) |
| `datos/alumnos_sucio.csv` | 22 | 1 fila por alumno (con duplicados) | Limpieza: mayúsculas, tildes, abreviaturas, comas decimales, `N/A`, `%` |

## Evaluación

Cada guía de ejercicios incluye comprobaciones automáticas (`OK` / `pendiente`).
Pauta sugerida para cada ejercicio:

| Criterio | Peso sugerido |
|---|---|
| El código se ejecuta sin errores en Colab y pasa la comprobación | 50 % |
| Usa el método adecuado (por ejemplo, `validate` en un merge, `groupby` antes de unir) | 25 % |
| Documenta las decisiones en celdas de texto (imputaciones, exclusiones, mapeos) | 25 % |

## Bibliografía y recursos

- Documentación oficial de pandas: <https://pandas.pydata.org/docs/>
- *10 minutes to pandas*: <https://pandas.pydata.org/docs/user_guide/10min.html>
- Guía de merge, join y concat: <https://pandas.pydata.org/docs/user_guide/merging.html>
- Google Colab: <https://colab.research.google.com>
