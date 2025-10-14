from queue import PriorityQueue

# Algoritmo voraz
# Recibe un diccionario de materias con sus cupos y un diccionario de estudiantes con la lista de materias a solicitar y prioridades
# Retorna un diccionario con las materias asignadas a cada estudiante
def rocV(materias, estudiantes):
    # Copia de estudiantes para no modificar el original
    # Ej: {"estudiante1": [(materia1, prioridad1), (materia2, prioridad2)], "estudiante2": [...], ...}
    estudiantesCopia = {}
    for estudiante in estudiantes:
        materiasDeEst = []
        for materia in estudiantes[estudiante]:
            materiasDeEst.append((materia[0], materia[1]))
        estudiantesCopia[estudiante] = materiasDeEst

    # Inicializar diccionario donde se almacenarán las materias dadas
    # Ej: {"estudiante1": [], ...}
    materiasDadas = {}
    for estudiante in estudiantes:
        materiasDadas[estudiante] = []

    # Construir la cola inicial (donde se almacenan las materias a asignar por prioridad y desempates, para tomar la mejor decisión en cada paso)
    cola = PriorityQueue()
    for estudiante in estudiantesCopia:
        for materiaId, prioridad in estudiantesCopia[estudiante]:
            numMatAsig = len(materiasDadas[estudiante]) # Número de materias ya asignadas
            numSolicitudes = len(estudiantesCopia[estudiante]) # Número de solicitudes restantes

            # Se inserta en la cola con prioridad negativa para que la cola tome 5 como mayor prioridad
            # Toma el menor numMatAsig, osea el que tiene menos materias asignadas
            # Toma el menor numSolicitudes, osea el que tiene menos solicitudes restantes
            cola.put((-prioridad, numMatAsig, numSolicitudes, estudiante, materiaId))

    # Lazy deletion
    while not cola.empty():
        mejorDecision = cola.get()
        prioridadNeg, numMatAsig, numSolicitudes, estudiante, materiaId = mejorDecision

        if numMatAsig != len(materiasDadas[estudiante]):
            continue

        # Verificar si el estudiante aún tiene esa materia en su lista
        materiaSigueDisponible = False
        for mat in estudiantesCopia[estudiante]:
            if mat[0] == materiaId:
                materiaSigueDisponible = True
                break
        if not materiaSigueDisponible:
            continue

        # Asignación si hay cupo
        if materias[materiaId] > 0:
            materiasDadas[estudiante].append(materiaId)
            materias[materiaId] -= 1

        # Quitar materia asignada o no disponible de su lista
        nuevasMaterias = []
        for mat in estudiantesCopia[estudiante]:
            if mat[0] != materiaId:
                nuevasMaterias.append(mat)
        estudiantesCopia[estudiante] = nuevasMaterias

        # Reinsertar el resto de materias del estudiante con valores actualizados
        for mat in estudiantesCopia[estudiante]:
            nuevaMateriaId = mat[0]
            nuevaPrioridad = mat[1]
            numMatAsigNuevo = len(materiasDadas[estudiante])
            numSolicitudesNuevo = len(estudiantesCopia[estudiante])

            cola.put((-nuevaPrioridad, numMatAsigNuevo, numSolicitudesNuevo, estudiante, nuevaMateriaId))

    return materiasDadas