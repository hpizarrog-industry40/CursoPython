# Curso de introducción a pandas

Proyecto para enseñar a un grupo de alumnos a usar la librería `pandas` de
Python, partiendo de archivos CSV reales. El curso se trabaja en **Google Colab**
(sin instalar nada) y también puede ejecutarse localmente con los scripts `.py`.

- 📘 Programa de estudio: [`PROGRAMA.md`](PROGRAMA.md)
- 📝 Notas para el docente: [`NOTAS_DOCENTE.md`](NOTAS_DOCENTE.md)

## Abrir en Google Colab

| Notebook | Unidades | Abrir |
|---|---|---|
| Parte 1: exploración, filtrado y faltantes | 1, 2 y 3 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hpizarrog-industry40/CursoPython/blob/main/Aprendiendo_Pandas/notebooks/Parte1_Pandas_Colab.ipynb) |
| Parte 2: combinación de tablas y limpieza | 4 y 5 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hpizarrog-industry40/CursoPython/blob/main/Aprendiendo_Pandas/notebooks/Parte2_Pandas_Colab.ipynb) |
| Parte 3: regresión lineal simple y múltiple | 6 | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hpizarrog-industry40/CursoPython/blob/main/Aprendiendo_Pandas/notebooks/Parte3_Regresion_Colab.ipynb) |

Los notebooks leen los datos directamente desde este repositorio, así que no hace
falta subir ningún archivo. Para guardar cambios: **Archivo → Guardar una copia en Drive**.

## Requisitos (ejecución local)

- Python 3.8 o superior
- pandas
- matplotlib, statsmodels y scikit-learn (solo para la unidad 6)

```
pip install -r requirements.txt
```

## Estructura del proyecto

```
Aprendiendo_Pandas/
|-- PROGRAMA.md                     Programa de estudio (unidades, sesiones, evaluación)
|-- NOTAS_DOCENTE.md                Ideas clave, errores frecuentes y preguntas por unidad
|-- datos/
|   |-- alumnos.csv                 Base principal (20 alumnos, notas y asistencia)
|   |-- cursos.csv                  Tabla auxiliar: profesor, sala y créditos por curso
|   |-- asistencia_mensual.csv      Asistencia por alumno y mes (otra granularidad)
|   |-- alumnos_2026_2.csv          Segundo período (para concatenar)
|   |-- alumnos_sucio.csv           Versión "sucia" de alumnos para practicar limpieza
|   `-- rendimiento.csv             150 estudiantes para regresión lineal
|-- ejemplos/
|   |-- 01_lectura_csv.py           Leer un CSV y primera inspección
|   |-- 02_exploracion_datos.py     info(), describe(), value_counts()
|   |-- 03_seleccion_filtrado.py    loc, iloc, filtros con condiciones
|   |-- 04_operaciones_columnas.py  Crear/renombrar/eliminar columnas, apply()
|   |-- 05_agrupacion.py            groupby(), agg(), sort_values()
|   |-- 06_valores_faltantes.py     isnull(), fillna(), dropna()
|   |-- 07_ordenar_exportar.py      sort_values() y to_csv()
|   |-- 08_merge_tablas.py          merge(), tipos de join, indicator, validate
|   |-- 09_granularidad_concat.py   Granularidad antes de unir; concat() de períodos
|   |-- 10_limpieza_datos.py        Limpieza paso a paso de un archivo real
|   |-- 11_funcion_limpieza.py      Funciones reutilizables, pipe() y registro
|   |-- 12_correlacion.py           corr() y diagramas de dispersión
|   |-- 13_regresion_simple.py      Recta, R², p-valor, predicción y residuos
|   |-- 14_regresion_multiple.py    Varias variables, C(), R² ajustado y VIF
|   `-- 15_prediccion_evaluacion.py train/test, MAE y RMSE con scikit-learn
|-- ejercicios/
|   |-- ejercicios_propuestos.py    Parte 1: ejercicios para los alumnos
|   |-- soluciones.py               Parte 1: soluciones (uso del profesor)
|   |-- ejercicios_parte2.py        Parte 2: ejercicios con comprobación automática
|   |-- soluciones_parte2.py        Parte 2: soluciones (uso del profesor)
|   |-- ejercicios_parte3.py        Parte 3: ejercicios guiados con comprobación
|   `-- soluciones_parte3.py        Parte 3: soluciones (uso del profesor)
`-- notebooks/
    |-- Parte1_Pandas_Colab.ipynb   Unidades 1-3 + ejercicios y soluciones
    |-- Parte2_Pandas_Colab.ipynb   Unidades 4-5 + ejercicios y soluciones
    `-- Parte3_Regresion_Colab.ipynb Unidad 6 + ejercicios guiados y soluciones
```

## Los datos

### `alumnos.csv` (base principal)

| Columna         | Descripción                                    |
|-----------------|------------------------------------------------|
| id              | Identificador del alumno (clave)               |
| nombre          | Nombre completo                                |
| edad            | Edad en años                                   |
| curso           | Matematicas, Fisica o Quimica                  |
| ciudad          | Ciudad de residencia (algunos valores vacíos)  |
| nota_parcial1   | Nota del primer parcial (0-10, algunos vacíos) |
| nota_parcial2   | Nota del segundo parcial (0-10, algunos vacíos)|
| nota_final      | Nota final (0-10)                              |
| asistencia      | Porcentaje de asistencia (0-100)               |

Tiene valores faltantes intencionados en `ciudad`, `nota_parcial1` y
`nota_parcial2` para enseñar cómo tratarlos (ver `ejemplos/06_valores_faltantes.py`).

### Tablas para las unidades 4, 5 y 6

- `cursos.csv`: una fila por curso (clave `curso`). Incluye *Biologia*, que no tiene alumnos, para mostrar `right_only` en un merge.
- `asistencia_mensual.csv`: tres filas por alumno (marzo, abril y mayo). Al unirla sin agregar, la base se triplica.
- `alumnos_2026_2.csv`: mismo formato que `alumnos.csv`. Salen los alumnos 10 y 18 y entran el 21 y el 22.
- `rendimiento.csv` (unidad 6): 150 estudiantes con horas de estudio, asistencia, horas de sueño (4 faltantes), si trabaja, curso y nota final. Datos simulados con relaciones conocidas para practicar regresión.
- `alumnos_sucio.csv`: los mismos 20 alumnos con 2 filas duplicadas, 15 formas de escribir los cursos, comas decimales, `N/A`, `-` y `%`. Tras limpiarlo con `11_funcion_limpieza.py` vuelve a coincidir con `alumnos.csv`.

## Cómo usar el proyecto en clase

### En Google Colab (recomendado)

Abra el notebook de la parte que corresponda con los botones de arriba y ejecute
las celdas en orden con **Shift + Enter**.

### En local

1. Ejecute los ejemplos en orden (del 01 al 15) desde la carpeta `Aprendiendo_Pandas`:

   ```
   cd Aprendiendo_Pandas
   python ejemplos/01_lectura_csv.py
   ...
   python ejemplos/15_prediccion_evaluacion.py
   ```

2. Los alumnos completan los ejercicios (los `TODO`):

   ```
   cd ejercicios
   python ejercicios_propuestos.py
   python ejercicios_parte2.py
   python ejercicios_parte3.py
   ```

3. El profesor compara con `soluciones.py`, `soluciones_parte2.py` y `soluciones_parte3.py`.

## Progresión sugerida

**Parte 1**
1. Qué es un DataFrame y cómo leer un CSV (`01`)
2. Explorar y entender los datos antes de trabajar con ellos (`02`)
3. Seleccionar y filtrar filas/columnas (`03`)
4. Crear y transformar columnas (`04`)
5. Agrupar y resumir datos (`05`)
6. Tratar datos faltantes, un problema real y frecuente (`06`)
7. Ordenar y exportar resultados (`07`)
8. Ejercicios propuestos de la parte 1

**Parte 2**
9. Unir la base principal con una tabla auxiliar (`08`)
10. Granularidad y concatenación de períodos (`09`)
11. Limpiar un archivo real paso a paso (`10`)
12. Automatizar la limpieza con funciones (`11`)
13. Ejercicios de la parte 2

**Parte 3**
14. Correlación y diagramas de dispersión (`12`)
15. Regresión lineal simple: recta, R² y residuos (`13`)
16. Regresión lineal múltiple y variables categóricas (`14`)
17. Predecir y evaluar con datos de prueba (`15`)
18. Ejercicios guiados de la parte 3
