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
    print(resultadosR)

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