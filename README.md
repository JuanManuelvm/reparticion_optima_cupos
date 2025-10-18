# Repartición Óptima de Cupos

Proyecto de curso para Análisis de Algoritmos II - Escuela de Ingeniería de Sistemas y Computación

## Descripción del Proyecto

Este proyecto implementa y compara tres estrategias algorítmicas diferentes para resolver el problema de asignación óptima de cupos de materias a estudiantes. El objetivo es minimizar la insatisfacción general de los estudiantes al asignar materias considerando sus prioridades y los cupos disponibles.

## El Problema

Cada semestre, los estudiantes enfrentan el desafío de matricularse en materias con cupos limitados. Este proyecto formaliza y resuelve el problema de distribución óptima mediante:

- **Entrada**: Conjunto de materias con cupos disponibles y solicitudes de estudiantes con prioridades asignadas
- **Salida**: Asignación de materias que minimiza la función de insatisfacción general
- **Restricciones**: Los estudiantes asignan prioridades (1-5) a cada materia solicitada, con un presupuesto total de prioridades definido por γ(X) = 3X - 1

## Métodos Implementados

El proyecto implementa tres enfoques algorítmicos:

1. **Fuerza Bruta (FB)**: Explora todas las soluciones posibles y selecciona la óptima. Garantiza encontrar la solución óptima pero tiene complejidad exponencial.

2. **Algoritmo Voraz (V)**: Utiliza una estrategia de selección greedy para asignar materias. Es eficiente pero no siempre garantiza la solución óptima.

3. **Programación Dinámica (PD)**: Aplica el principio de optimalidad de Bellman para construir soluciones óptimas a partir de subproblemas. Garantiza optimalidad con mejor eficiencia que fuerza bruta.

## Estructura del Proyecto
```
reparticion_optima_cupos/
├── Dinamica/           # Implementación de programación dinámica
├── FuerzaBruta/        # Implementación de fuerza bruta
├── Input_output/       # Módulos de lectura/escritura de archivos
├── Pruebas/            # Casos de prueba
├── Voraz/              # Implementación del algoritmo voraz
├── main.py             # Punto de entrada de la aplicación
├── README.md           # Este archivo
└── .gitignore
```

## Requisitos

- Python 3.x
- tkinter (incluido en la mayoría de instalaciones de Python)

## Instalación

Clonar el repositorio:
```bash
git clone https://github.com/usuario/reparticion_optima_cupos.git
cd reparticion_optima_cupos
```

## Ejecución

Para ejecutar la aplicación con interfaz gráfica:
```bash
python main.py
```

## Uso de la Aplicación

1. **Cargar datos**: Haga clic en "Cargar Archivo .txt" y seleccione un archivo de entrada con el formato especificado
2. **Seleccionar algoritmo**: Elija entre Fuerza Bruta, Voraz o Dinámico
3. **Ejecutar**: Presione "Ejecutar Algoritmo Seleccionado"
4. **Ver resultados**: Los resultados se mostrarán en las pestañas correspondientes

## Formato de Archivos

### Archivo de Entrada
```
k
M1,m1
M2,m2
...
Mk,mk
r
e1,s1
m11,p11
m12,p12
...
```

Donde:
- k: número de materias
- Mi,mi: código de materia y cupo disponible
- r: número de estudiantes
- ej,sj: código de estudiante y número de materias solicitadas
- mij,pij: código de materia solicitada y prioridad asignada

### Archivo de Salida
```
Costo
e1,a1
m11
m12
...
```

Donde:
- Costo: valor de la función de insatisfacción
- ej,aj: código de estudiante y número de materias asignadas
- mij: código de materia asignada

## Función de Insatisfacción

La insatisfacción de cada estudiante se calcula como:
```
fj = (1 - |maj|/|msj|) * (Σ prioridades no asignadas / γ(|msj|))
```

La insatisfacción general es el promedio de las insatisfacciones individuales.


## Autores

Proyecto desarrollado para el curso de Análisis de Algoritmos II

Fernando Cardona Giraldo - 2241381
Juan Manuel Vargas - 2438185
Pablo Esteban Becerra - 2243506

## Docente

Profesor: Jesús Alexander Aranda Ph.D


## Fecha de Entrega

14 de octubre de 2025

## Licencia

Este proyecto es de uso académico para la Universidad del Valle.
