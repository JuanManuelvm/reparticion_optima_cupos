from input_output.salida import calcularInsatisfaccionGeneral

def combinaciones(materias, solicitudes):

    alumnos = list(solicitudes.keys())
    todas_las_combinaciones = []

    def recursiva(i, materias_restantes, asignaciones):
        # Si todos los alumnos fueron procesados, guardar copia
        if i == len(alumnos):
            todas_las_combinaciones.append({a: m.copy() for a, m in asignaciones.items()})
            return
        
        alumno = alumnos[i]
        opciones = solicitudes[alumno]
        asignaciones[alumno] = []

        # Función para probar todas las combinaciones de materias de este alumno
        def asignar_materias(j, materias_restantes_local):
            if j == len(opciones):
                recursiva(i + 1, materias_restantes_local, asignaciones)
                return
            
            materia, _ = opciones[j]

            # Caso 1: no tomar esta materia
            asignar_materias(j + 1, materias_restantes_local.copy())

            # Caso 2: tomarla si hay cupos
            if materias_restantes_local[materia] > 0:
                materias_restantes_local[materia] -= 1
                asignaciones[alumno].append(materia)

                asignar_materias(j + 1, materias_restantes_local.copy())

                asignaciones[alumno].pop()

        asignar_materias(0, materias_restantes.copy())

        del asignaciones[alumno]

    recursiva(0, materias.copy(), {})
    return todas_las_combinaciones

def rocFB(materias, estudiantes):
    materiasAsignadas = combinaciones(materias, estudiantes)
    insatisfaccion = []
    menor = 100
    combinacion = 0
    for i in materiasAsignadas:
        individual = calcularInsatisfaccionGeneral(i, estudiantes, materias)
        insatisfaccion.append(individual)
        if individual <= menor:
            combinacion = i
            menor = individual

    #print(menor)
    #print(combinacion)
    return combinacion, menor