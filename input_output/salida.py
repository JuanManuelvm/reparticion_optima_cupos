import os

def calcularInsatisfaccionGeneral(materiasDadas, estudiantes, materias):
    insatisfaccionesIndividuales = calcularInsatisfaccionIndividual(materiasDadas, estudiantes, materias)
    suma = 0
    for insatisfaccion in insatisfaccionesIndividuales:
        suma += insatisfaccion
    insatisfaccionGeneral = suma / len(insatisfaccionesIndividuales)
    return insatisfaccionGeneral

def calcularInsatisfaccionIndividual(materiasDadas, estudiantes, materias):
    primerosFactores = []
    for estudiante in estudiantes:
        numeroDeMateriasSolicitadas = len(estudiantes[estudiante])
        numeroDeMateriasAsignadas = len(materiasDadas[estudiante])
        primerFactor = (1 - (numeroDeMateriasAsignadas / numeroDeMateriasSolicitadas))
        primerosFactores.append(primerFactor)

    materiasNoAsignadas = tomarMateriasNoAsignadas(materiasDadas, estudiantes)
    sumas = sumarPrioridades(materiasNoAsignadas)
    resultadosR = formulaR(estudiantes)
    #print(resultadosR)

    segundosFactores = []
    for indice, valor in enumerate(sumas):
        segundoFactor = valor / resultadosR[indice]
        segundosFactores.append(segundoFactor)

    resultados = []
    for indice, valor in enumerate(primerosFactores):
        resultado = valor * segundosFactores[indice]
        resultados.append(resultado)

    return resultados

def tomarMateriasNoAsignadas(materiasDadas, estudiantes):
    materiasNoAsignadas = {}
    for estudiante in estudiantes:
        materiasNoAsignadas[estudiante] = []
        materiasSiAsignadas = materiasDadas[estudiante]
        materiasSolicitadas = estudiantes[estudiante]

        for materiaSolicitada in materiasSolicitadas:
            materia, prioridad = materiaSolicitada
            if materia not in materiasSiAsignadas:
                materiasNoAsignadas[estudiante].append((materia, prioridad)) 
    
    return materiasNoAsignadas

def sumarPrioridades(materiasNoAsignadas):
    sumas = []
    for estudiante in materiasNoAsignadas:
        sumarPrioridades = 0
        for materia in materiasNoAsignadas[estudiante]:
            materiaId, prioridad = materia
            sumarPrioridades += prioridad
        sumas.append(sumarPrioridades)
    return sumas

def formulaR(estudiantes):
    resultadosR = []
    for estudiante in estudiantes:
        numeroDeMateriasSolicitadas = len(estudiantes[estudiante])
        r = (3 * numeroDeMateriasSolicitadas) - 1
        resultadosR.append(r)
    return resultadosR

"""
Crea un archivo .txt en la carpeta especificada con el formato:
    
Costo
e1,a1
m11
m12
...
e2,a2
...
    
Parámetros:
    ruta_carpeta (str): ruta de la carpeta donde guardar el archivo.
    nombre_archivo (str): nombre del archivo (ej: 'Resultado1.txt')
    materiasAsignadas (dict): diccionario {estudiante: [materias_asignadas]}
    insatisfaccionGeneral (float o int): valor de la insatisfacción general.
"""
def guardar_resultados(ruta_carpeta, nombre_archivo, materiasAsignadas, insatisfaccionGeneral):
    
    # Crear carpeta si no existe
    os.makedirs(ruta_carpeta, exist_ok=True)

    # Ruta completa del archivo
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

    # Escribir contenido
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        # Primera línea: costo (insatisfacción)
        f.write(f"{round(insatisfaccionGeneral, 3)}\n")

        # Por cada estudiante, imprimir su info
        for estudiante, materias in materiasAsignadas.items():
            # Línea con id del estudiante y número de materias
            f.write(f"{estudiante},{len(materias)}\n")

            # Luego cada materia en una línea
            for materia in materias:
                f.write(f"{materia}\n")

    print(f"✅ Archivo creado en: {ruta_completa}")