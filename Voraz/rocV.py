#Debe ir el algoritmo voraz
from queue import PriorityQueue


# Forma de chat gpt 1
# def rocV(materias, estudiantes):
#     print(materias)
#     print(estudiantes)

#     estudiantesCopia = {k: v.copy() for k, v in estudiantes.items()}

#     # Asignar los estudiantes al diccionario de materias dadas (donde se guardan las materias asignadas a cada estudiante)
#     materiasDadas = {}

#     for estudiante in estudiantes:
#         materiasDadas[estudiante] = []

#     cola = PriorityQueue()
#     cola = construirCola(cola, estudiantes, materiasDadas)

#     while True:
#         if cola.empty():
#             print("pare")
#             break
#         materiaConMayorPrioridad = cola.get()
#         print(materiaConMayorPrioridad)
#         estudiante, materiaId = materiaConMayorPrioridad[3]

#         if materias[materiaId] > 0:
#             print("asigno")
#             materiasDadas[estudiante].append(materiaId)
#             materias[materiaId] -= 1
#             nuevoEstudiantes = quitarMateriaYaDadaDeEstudiante(estudiantesCopia, materiaId, estudiante)
#             cola = construirCola(cola, nuevoEstudiantes, materiasDadas)
#         else:
#             print("elimino")
#             nuevoEstudiantes = quitarMateriaYaDadaDeEstudiante(estudiantesCopia, materiaId, estudiante)
#             cola = construirCola(cola, nuevoEstudiantes, materiasDadas)

#     return materiasDadas

# def primerDesempate(materiasDadas, estudiante):
#     numMateriasAsignadas = len(materiasDadas[estudiante])
#     return numMateriasAsignadas

# def segundoDesempate(estudiantes, estudiante):
#     numSolicitudes = len(estudiantes[estudiante])
#     return numSolicitudes 

# def tercerDesempate(estudiantes, estudiante):
#     sumaDePrioridades = 0
#     materias = estudiantes[estudiante]
#     for materia in materias:
#         materiaId, prioridad = materia
#         sumaDePrioridades += prioridad
#     return sumaDePrioridades

# def construirCola(cola, estudiantes, materiasDadas):
#     cola = PriorityQueue()
#     for estudiante in estudiantes:
#         materiasSolicitadas = estudiantes[estudiante]
#         for materia in materiasSolicitadas:
#             materiaId, prioridad = materia
#             numMateriasAsignadas = primerDesempate(materiasDadas, estudiante)
#             numSolicitudes = segundoDesempate(estudiantes, estudiante)
#             #sumaDePrioridades = tercerDesempate(estudiantes, estudiante)
#             cola.put((numMateriasAsignadas/numSolicitudes if numSolicitudes > 0 else 0, -prioridad, numMateriasAsignadas,(estudiante, materiaId)))
#     return cola

# def quitarMateriaYaDadaDeEstudiante(estudiantesCopia, materiaID, estudiante):
#     materias = estudiantesCopia[estudiante]
#     prioridadDeLaMateria = 0
#     for materia in materias:
#         materiaId, prioridad = materia
#         if materiaId == materiaID:
#             prioridadDeLaMateria = prioridad
#             break
#     estudiantesCopia[estudiante].remove((materiaID, prioridadDeLaMateria))
#     return estudiantesCopia

# El inicial
# def rocV(materias, estudiantes):
#     print(materias)
#     print(estudiantes)

#     # Hacer una copia del diccionario de estudiantes para no modificar el original
#     estudiantesCopia = {k: v.copy() for k, v in estudiantes.items()}

#     # Asignar los estudiantes al diccionario de materias dadas (donde se guardan las materias asignadas a cada estudiante)
#     materiasDadas = {}

#     for estudiante in estudiantes:
#         materiasDadas[estudiante] = []

#     cola = PriorityQueue()
#     cola = construirCola(cola, estudiantesCopia, materiasDadas)

#     while True:
#         if cola.empty():
#             print("pare")
#             break
#         materiaConMayorPrioridad = cola.get()
#         print(materiaConMayorPrioridad)
#         estudiante, materiaId = materiaConMayorPrioridad[4]

#         if materias[materiaId] > 0:
#             print("asigno")
#             materiasDadas[estudiante].append(materiaId)
#             materias[materiaId] -= 1
#             nuevoEstudiantes = quitarMateriaYaDadaDeEstudiante(estudiantesCopia, materiaId, estudiante)
#             cola = construirCola(cola, nuevoEstudiantes, materiasDadas)
#         else:
#             print("elimino")
#             nuevoEstudiantes = quitarMateriaYaDadaDeEstudiante(estudiantesCopia, materiaId, estudiante)
#             cola = construirCola(cola, nuevoEstudiantes, materiasDadas)

#     return materiasDadas

# def primerDesempate(materiasDadas, estudiante):
#     numMateriasAsignadas = len(materiasDadas[estudiante])
#     return numMateriasAsignadas

# def segundoDesempate(estudiantes, estudiante):
#     numSolicitudes = len(estudiantes[estudiante])
#     return numSolicitudes 

# def tercerDesempate(estudiantes, estudiante):
#     sumaDePrioridades = 0
#     materias = estudiantes[estudiante]
#     for materia in materias:
#         materiaId, prioridad = materia
#         sumaDePrioridades += prioridad
#     return sumaDePrioridades

# def construirCola(cola, estudiantes, materiasDadas):
#     cola = PriorityQueue()
#     for estudiante in estudiantes:
#         materiasSolicitadas = estudiantes[estudiante]
#         for materia in materiasSolicitadas:
#             materiaId, prioridad = materia
#             numMateriasAsignadas = primerDesempate(materiasDadas, estudiante)
#             numSolicitudes = segundoDesempate(estudiantes, estudiante)
#             sumaDePrioridades = tercerDesempate(estudiantes, estudiante)
#             cola.put((-prioridad, numMateriasAsignadas, numSolicitudes, -sumaDePrioridades, (estudiante, materiaId)))
#     return cola

# def quitarMateriaYaDadaDeEstudiante(estudiantesCopia, materiaID, estudiante):
#     materias = estudiantesCopia[estudiante]
#     prioridadDeLaMateria = 0
#     for materia in materias:
#         materiaId, prioridad = materia
#         if materiaId == materiaID:
#             prioridadDeLaMateria = prioridad
#             break
#     estudiantesCopia[estudiante].remove((materiaID, prioridadDeLaMateria))
#     return estudiantesCopia


# Algoritmo voraz
# Recibe un diccionario de materias con sus cupos y un diccionario de estudiantes con la lista de materias a solicitar y prioridades
# Retorna un diccionario con las materias asignadas a cada estudiante
def rocV(materias, estudiantes):

    # Copia de estudiantes para no modificar el original
    # Ej: {"estudiante1": [(materia1, prioridad1), (materia2, prioridad2)], "estudiante2": [...], ...}
    estudiantesCopia = {}
    for estudiante in estudiantes:
        materiasEst = []
        for materia in estudiantes[estudiante]:
            materiasEst.append((materia[0], materia[1]))
        estudiantesCopia[estudiante] = materiasEst

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
            sumaPrioridades = 0 # Suma de prioridades de las materias restantes
            for m in estudiantesCopia[estudiante]:
                sumaPrioridades += m[1]

            # Se inserta en la cola con prioridad negativa para que la cola tome 5 como mayor prioridad
            # Toma el menor numMatAsig, osea el que tiene menos materias asignadas
            # Toma el menor numSolicitudes, osea el que tiene menos solicitudes restantes
            # Toma la mayor sumaPrioridades, osea el que tiene mayor suma de prioridades restantes 
            cola.put((-prioridad, numMatAsig, numSolicitudes, -sumaPrioridades, estudiante, materiaId))

    # Lazy deletion
    while not cola.empty():
        elemento = cola.get()
        prioridadNeg, numMatAsig, numSolicitudes, sumaNeg, estudiante, materiaId = elemento

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
            #print("asigno:", estudiante, "→", materiaId)
            materiasDadas[estudiante].append(materiaId)
            materias[materiaId] -= 1
        else:
            f = 0
            #print("elimino:", estudiante, "→", materiaId)

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
            sumaPrioridadesNueva = 0
            for m in estudiantesCopia[estudiante]:
                sumaPrioridadesNueva += m[1]

            cola.put((
                -nuevaPrioridad,
                numMatAsigNuevo,
                numSolicitudesNuevo,
                -sumaPrioridadesNueva,
                estudiante,
                nuevaMateriaId
            ))

    return materiasDadas