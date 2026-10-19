# Programa de estudio — Programación en Python: análisis de datos con Pandas

| | |
|---|---|
| **Asignatura** | Programación en Python |
| **Módulo** | Manipulación y preparación de datos con Pandas (Solemne 1) |
| **Herramienta de trabajo** | Google Colab (navegador + cuenta Google, sin instalación) |
| **Material** | Este repositorio: `datos/`, `ejemplos/`, `ejercicios/`, `notebooks/` |
| **Librerías** | pandas, matplotlib, statsmodels, scikit-learn y xgboost (todas preinstaladas en Colab) |
| **Requisito previo** | Python básico: variables, listas, diccionarios, funciones, `if` y `for` |

## Resultado de aprendizaje general

Al terminar el módulo, el estudiante prepara una base de datos real para el análisis:
la carga y explora, filtra y ordena según una pregunta, crea variables derivadas,
trata los datos faltantes de forma justificada, integra varias tablas sin perder
trazabilidad, automatiza la limpieza con funciones reutilizables y construye e
interpreta modelos de regresión lineal simple y múltiple, y anticipa resultados con
modelos de árboles (árbol de decisión, Random Forest y XGBoost) y forecasting semanal.

## Unidades

| # | Unidad | Objetivo de aprendizaje | Contenidos | Material | Evidencia |
|---|---|---|---|---|---|
| 1 | Introducción a Pandas: DataFrames, carga de datos y exploración inicial | Usar DataFrames para describir y explorar bases de datos | `read_csv`, `head`, `tail`, `shape`, `info`, `describe`, `dtypes`, `value_counts`, selección de columnas, primeras validaciones | `01_lectura_csv.py`, `02_exploracion_datos.py` | Ejercicio 4 (parte 1) |
| 2 | Filtrado, ordenamiento, selección y transformación | Filtrar observaciones relevantes y ordenar datos según preguntas analíticas | `loc`, `iloc`, máscaras booleanas, `&`, `\|`, `isin`, `sort_values`, `groupby` + `mean` | `03_seleccion_filtrado.py`, `05_agrupacion.py`, `07_ordenar_exportar.py` | Ejercicios 1, 2 y 3 (parte 1) |
| 3 | Transformación de datos y tratamiento de valores faltantes | Crear variables derivadas y tratar datos faltantes de forma documentada | Columnas calculadas, `apply`, `rename`, `drop`, `isnull`, `fillna`, `dropna`, registro de decisiones | `04_operaciones_columnas.py`, `06_valores_faltantes.py` | Ejercicio 5 (parte 1) + registro de decisiones |
| 4 | Combinación de tablas: joins, merges y concatenaciones | Integrar varias tablas respetando claves, granularidad y trazabilidad | `merge` (`on`, `how`, `left_on/right_on`), tipos de join, `indicator`, `validate`, granularidad, `groupby` antes de unir, `concat`, columna de período, `pivot_table` | `08_merge_tablas.py`, `09_granularidad_concat.py` | Ejercicios 1 a 4 (parte 2) |
| 5 | Limpieza de datos reales y automatización simple de tareas rutinarias | Diseñar un flujo reutilizable de limpieza y preparación de datos | Nombres de columnas, `drop_duplicates`, métodos `.str`, quitar tildes, mapeo de categorías, `to_numeric(errors="coerce")`, funciones, `.pipe()`, registro de limpieza, `assert` | `10_limpieza_datos.py`, `11_funcion_limpieza.py` | Ejercicio 5 (parte 2) |
| 6 | Uso estadístico con Python | Construir, interpretar y evaluar modelos de regresión lineal simple y múltiple | Correlación (`corr`), diagramas de dispersión, `smf.ols` con fórmulas, coeficientes, p-valor, R² y R² ajustado, residuos, variables categóricas `C()`, multicolinealidad (VIF), `train_test_split`, MAE y RMSE | `12_correlacion.py`, `13_regresion_simple.py`, `14_regresion_multiple.py`, `15_prediccion_evaluacion.py` | Ejercicios guiados 1 a 5 (parte 3) + interpretación escrita |
| 7 | Modelos de predicción con árboles y forecasting | Clasificar y pronosticar con árbol de decisión, Random Forest y XGBoost, evaluando con datos no vistos y respetando el orden temporal | Clasificación vs. regresión, `DecisionTreeClassifier`, `max_depth` y sobreajuste, matriz de confusión, exactitud, recall, AUC, `RandomForestClassifier`, importancia por impureza y por permutación, `XGBClassifier`/`XGBRegressor` e hiperparámetros, alerta temprana, rezagos (`shift`), medias móviles (`rolling`), variables de calendario, división temporal, líneas base y MAE | `16_arbol_decision.py`, `17_random_forest.py`, `18_xgboost_alerta_temprana.py`, `19_forecasting_semanal.py` | Ejercicios guiados 1 a 5 (parte 4) + interpretación escrita |

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
| 7 | Unidad 6: correlación y regresión simple | `notebooks/Parte3_Regresion_Colab.ipynb` (secciones 1 y 2) | Graficar, calcular r, ajustar la recta e interpretar la pendiente con una frase |
| 8 | Unidad 6: regresión múltiple y evaluación | Parte 3 (secciones 3 y 4) | Comparar modelos con R² ajustado, leer coeficientes y evaluar con datos de prueba |
| 9 | Práctica parte 3 | Parte 3 (ejercicios guiados y soluciones) | Ejercicios guiados 1–5 y celda de interpretación |
| 10 | Unidad 7: árbol de decisión y Random Forest | `notebooks/Parte4_Arboles_Forecasting_Colab.ipynb` (secciones 1 y 2) | Leer las reglas del árbol, detectar el sobreajuste y comparar medidas de importancia |
| 11 | Unidad 7: XGBoost y forecasting | Parte 4 (secciones 3 y 4) | Construir la alerta temprana de la semana 6 y pronosticar el control semanal con división temporal |
| 12 | Práctica parte 4 | Parte 4 (ejercicios guiados y soluciones) | Ejercicios guiados 1–5 y celda de interpretación |

## Datos del curso

| Archivo | Filas | Granularidad | Uso |
|---|---|---|---|
| `datos/alumnos.csv` | 20 | 1 fila por alumno | Base principal (unidades 1–4) |
| `datos/cursos.csv` | 4 | 1 fila por curso | Tabla auxiliar para `merge` (incluye *Biologia*, sin alumnos) |
| `datos/asistencia_mensual.csv` | 60 | 1 fila por alumno y mes | Ejemplo de granularidad distinta |
| `datos/alumnos_2026_2.csv` | 20 | 1 fila por alumno | Segundo período para `concat` (2 alumnos salen, 2 entran) |
| `datos/alumnos_sucio.csv` | 22 | 1 fila por alumno (con duplicados) | Limpieza: mayúsculas, tildes, abreviaturas, comas decimales, `N/A`, `%` |
| `datos/rendimiento.csv` | 150 | 1 fila por estudiante | Regresión: horas de estudio, asistencia, horas de sueño (4 faltantes), trabaja, curso y nota final |
| `datos/seguimiento_semanal.csv` | 2.400 | 1 fila por estudiante y semana (16 semanas) | Árboles y forecasting: horas de estudio, asistencia, entrega de tarea y nota del control semanal; certámenes en las semanas 8 y 16 |

## Evaluación

Cada guía de ejercicios incluye comprobaciones automáticas (`OK` / `pendiente`).
Pauta sugerida para cada ejercicio:

| Criterio | Peso sugerido |
|---|---|
| El código se ejecuta sin errores en Colab y pasa la comprobación | 50 % |
| Usa el método adecuado (por ejemplo, `validate` en un merge, `groupby` antes de unir) | 25 % |
| Documenta las decisiones en celdas de texto (imputaciones, exclusiones, mapeos, interpretación de coeficientes) | 25 % |

## Bibliografía y recursos

- Documentación oficial de pandas: <https://pandas.pydata.org/docs/>
- *10 minutes to pandas*: <https://pandas.pydata.org/docs/user_guide/10min.html>
- Guía de merge, join y concat: <https://pandas.pydata.org/docs/user_guide/merging.html>
- Google Colab: <https://colab.research.google.com>
- Regresión con fórmulas en statsmodels: <https://www.statsmodels.org/stable/example_formulas.html>
- Regresión lineal en scikit-learn: <https://scikit-learn.org/stable/modules/linear_model.html>
- Árboles de decisión en scikit-learn: <https://scikit-learn.org/stable/modules/tree.html>
- Random Forest y otros ensambles: <https://scikit-learn.org/stable/modules/ensemble.html>
- Documentación de XGBoost: <https://xgboost.readthedocs.io/>
