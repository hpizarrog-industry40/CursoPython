# Curso de introduccion a pandas

Proyecto de ejemplo para ensenar a un grupo de alumnos a usar la libreria
`pandas` de Python, partiendo de un archivo CSV real.

## Requisitos

- Python 3.8 o superior
- pandas

Instalar dependencias:

```
pip install -r requirements.txt
```

## Estructura del proyecto

```
Aprendiendo_Pandas/
|-- datos/
|   `-- alumnos.csv          Dataset de ejemplo (20 alumnos, notas y asistencia)
|-- ejemplos/
|   |-- 01_lectura_csv.py           Leer un CSV y primera inspeccion
|   |-- 02_exploracion_datos.py     info(), describe(), value_counts()
|   |-- 03_seleccion_filtrado.py    loc, iloc, filtros con condiciones
|   |-- 04_operaciones_columnas.py  Crear/renombrar/eliminar columnas, apply()
|   |-- 05_agrupacion.py            groupby(), agg(), sort_values()
|   |-- 06_valores_faltantes.py     isnull(), fillna(), dropna()
|   `-- 07_ordenar_exportar.py      sort_values() y to_csv()
`-- ejercicios/
    |-- ejercicios_propuestos.py    Ejercicios para que resuelvan los alumnos
    `-- soluciones.py               Soluciones (uso del profesor)
```

## El dataset (`datos/alumnos.csv`)

Contiene 20 alumnos con las columnas:

| Columna         | Descripcion                                  |
|-----------------|-----------------------------------------------|
| id              | Identificador del alumno                      |
| nombre          | Nombre completo                               |
| edad            | Edad en anios                                 |
| curso           | Matematicas, Fisica o Quimica                 |
| ciudad          | Ciudad de residencia (algunos valores vacios) |
| nota_parcial1   | Nota del primer parcial (0-10)                |
| nota_parcial2   | Nota del segundo parcial (0-10, algunos vacios)|
| nota_final      | Nota final (0-10)                             |
| asistencia      | Porcentaje de asistencia (0-100)              |

Tiene valores faltantes intencionados en `ciudad` y `nota_parcial2` para
poder ensenar como tratarlos (ver `ejemplos/06_valores_faltantes.py`).

## Como usar el proyecto en clase

1. Ejecutar los ejemplos en orden (del 01 al 07), leyendo los comentarios
   de cada archivo:

   ```
   cd Aprendiendo_Pandas
   python ejemplos/01_lectura_csv.py
   python ejemplos/02_exploracion_datos.py
   ...
   ```

2. Cada archivo es independiente y esta comentado paso a paso, ideal para
   proyectarlo y explicarlo linea por linea.

3. Al terminar los ejemplos, los alumnos completan
   `ejercicios/ejercicios_propuestos.py` (los `TODO`), y ejecutan:

   ```
   cd ejercicios
   python ejercicios_propuestos.py
   ```

4. El profesor puede comparar con `ejercicios/soluciones.py`.

## Sugerencia de progresion (sesion de clase)

1. Que es un DataFrame y como leer un CSV (`01`)
2. Explorar y entender los datos antes de trabajar con ellos (`02`)
3. Seleccionar y filtrar filas/columnas (`03`)
4. Crear y transformar columnas (`04`)
5. Agrupar y resumir datos (`05`)
6. Tratar datos faltantes, un problema real y frecuente (`06`)
7. Ordenar y exportar resultados (`07`)
8. Practica libre con los ejercicios propuestos
