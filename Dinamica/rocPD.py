# logica.py
# ========================================
# Contiene TODA la lógica de cálculo, lectura de archivos y validaciones
# ========================================

from itertools import combinations

def calcular_gamma(num_materias):
    """Calcula gamma(X) = 3X - 1"""
    return 3 * num_materias - 1


def calcular_insatisfaccion_estudiante(materias_solicitadas, materias_asignadas):
    """
    Calcula la función de insatisfacción de un estudiante j:
    fj = (1 - |maj|/|msj|) * (Σ prioridades no asignadas / y(|msj|))
    """
    num_solicitadas = len(materias_solicitadas)
    num_asignadas = len(materias_asignadas)

    if num_solicitadas == 0:
        return 0.0

    gamma_value = calcular_gamma(num_solicitadas)
    codigos_asignados = {codigo for codigo, _ in materias_asignadas}

    suma_prioridades_no_asignadas = sum(
        prioridad for codigo, prioridad in materias_solicitadas if codigo not in codigos_asignados
    )

    factor_materias = 1 - (num_asignadas / num_solicitadas)
    factor_prioridades = suma_prioridades_no_asignadas / gamma_value
    return factor_materias * factor_prioridades


def calcular_insatisfaccion_general(M, E, A):
    """
    Calcula F<M,E>(A) = (Σ fj) / r
    """
    r = len(E)
    if r == 0:
        return 0.0

    asignaciones_dict = {codigo_est: materias_asig for codigo_est, materias_asig in A}
    suma_insatisfacciones = 0.0

    for codigo_est, materias_solicitadas in E:
        materias_asignadas = asignaciones_dict.get(codigo_est, [])
        fj = calcular_insatisfaccion_estudiante(materias_solicitadas, materias_asignadas)
        suma_insatisfacciones += fj

    return suma_insatisfacciones / r






def rocPD(k, r, M, E):
    """
    Algoritmo de Programación Dinámica con memoización MANUAL para asignar materias.
    
    Parámetros:
    - k: número de materias disponibles
    - r: número de estudiantes
    - M: lista de (codigo_materia, cupo)
    - E: lista de (codigo_estudiante, [(codigo_materia, prioridad), ...])
    
    Retorna:
    - A: asignaciones optimas
    - costo_normalizado: insatisfacción general mínima
    """
    
    # Mapeo de códigos a índices numéricos 
    # haces un umpaking de los codigos de M y los agrega a la lista codigos, despues la ordena con sort()
    codigos = [] # -> [101, 102, 103, 104]
    for codigo, _ in M:
        codigos.append(codigo)
    codigos.sort()
    

    # aca se mapea cada codigo a su indice en la lista codigos, esto para tener una representacion mas compacta
    # esto con el fin de pasar a busquedad de O(n) a O(1)
    # codigo_a_idx = {101: 0, 102: 1, 103: 2, 104: 3}
    codigo_a_idx = {}
    for i in range(len(codigos)):
        codigo_a_idx[codigos[i]] = i
    


    # se organizan los cupos en una tupla de manera que queden con el mismo orden que los codigos para que esten sincronizados
    # M_ordenado = [(101, 2), (102, 1), (103, 1), (104, 1)]
    M_ordenado = sorted(M, key=lambda x: x[0])
    cupos_lista = []
    for _, cupo in M_ordenado:
        cupos_lista.append(cupo)
    cupos_iniciales = tuple(cupos_lista) #-> (2, 1, 1, 1)
    


    # se almacena en estudiantes 
    estudiantes = [] # -> [(201, [(0, 1), (1, 2)], [(101, 1), (102, 2)]), (202, [(1, 1), (2, 2)], [(102, 1), (103, 2)]), ...]
    for codigo_est, materias_solicitadas in E:
        materias_idx = [] # -> [(0, 1), (1, 2)]  (codigo 101 con prioridad 1, codigo 102 con prioridad 2)
        for codigo, pref in materias_solicitadas:
            materias_idx.append((codigo_a_idx[codigo], pref))
        estudiantes.append((codigo_est, materias_idx, materias_solicitadas))
    


    combinaciones = []
    # estudiantes[n] = (codigo_est, materias_idx, materias_solicitadas)
    for _, materias_idx, _ in estudiantes:
        # combos es una lista de todas las combinaciones posibles de materias que el estudiante puede solicitar
        combos = [] # -> [[], [(0, 1)], [(1, 2)], [(0, 1), (1, 2)]]
        n = len(materias_idx)
        for tam in range(n + 1):
            for comb in combinations(materias_idx, tam):
                combos.append(list(comb))
        combinaciones.append(combos)
    
    # ============================================================================
    # FASE 2: PROGRAMACION DINÁMICA CON MEMOIZACION
    # ============================================================================
    
    # diccionario para memoizacion: guarda resultados de estados ya calculados
    # clave: (j, cupos) donde j es indice de estudiante y cupos es tupla de cupos restantes
    # valor: (mejor_asignacion, mejor_costo) solucion optima para ese estado
    memo = {}  # -> {(0, (2,1,1,1)): ([...], 1.5), (1, (1,0,1,1)): ([...], 0.8), ...}
    
    def dp(j, cupos):
        """
        funcion recursiva que implementa programación dinamica con memoizacion.
        
        resuelve el subproblema: ¿cuál es la asignación optima para los estudiantes
        desde j hasta el final, dado que tenemos 'cupos' disponibles?
        
        Parámetros:
        - j: indice del estudiante actual (de 0 a len(estudiantes)-1)
        - cupos: tupla con cupos restantes de cada materia (indice i = materia i)

                ejemplo: (2, 1, 0, 3) significa mat[0]=2 cupos, mat[1]=1, mat[2]=0, mat[3]=3
        
        Retorna:
        - (mejor_asignacion, mejor_costo): tupla con la asignación optima y su costo
        mejor_asignacion: estructura recursiva ((materias_est_j, resto_asignaciones))
        mejor_costo: float con la insatisfacción total acumulada
        
        estado del DP:
        - espacio de estados: (j, cupos) con j ∈ [0, n] y cupos ∈ ∏[0, Ci]
        - subestructura optima: solución optima de (j, cupos) se construye de (j+1, cupos_actualizados)
        - solapamiento: el mismo estado (j, cupos) puede alcanzarse por multiples caminos
        """
        
        # PASO 1: verificar memoizacion
        # crear clave unica para el estado actual (j, cupos)
        clave = (j, cupos)
        
        # si ya calculamos este estado antes, devolver resultado guardado (cache hit)
        if clave in memo:
            return memo[clave]  # O(1) - evita recalcular
        
        # PASO 2: caso base
        # si ya procesamos todos los estudiantes, no hay mas insatisfaccion que agregar
        if j == len(estudiantes):
            resultado = ([], 0.0)  # (asignaciones_vacías, costo_cero)
            memo[clave] = resultado  # guardar en memo
            return resultado
        
        # PASO 3: caso recursivo
        # obtener información del estudiante actual
        codigo_est, materias_idx, materias_solicitadas = estudiantes[j]
        #            ↑               ↑
        #            indices         codigos originales
        
        # inicializar busqueda de la mejor opcion
        mejor_costo = float("inf")  # empezar con costo infinito
        mejor_asignacion = None     # no hay asignacion aun
        
        # PASO 4: explorar todas las combinaciones posibles para el estudiante j
        # combinaciones[j] = [[], [(0,p1)], [(1,p2)], [(0,p1),(1,p2)], ...]
        for combinacion in combinaciones[j]:
            # combinacion es una posible asignación: ej. [(0, 0.9), (2, 0.7)]
            #                                              ↑         ↑
            #                                          índice_mat  prioridad
            
            # SUB-PASO 4.1: verificar disponibilidad de cupos
            # revisar que TODAS las materias en la combinacion tengan cupo > 0
            tiene_cupo = True
            for mat_idx, _ in combinacion:
                if cupos[mat_idx] <= 0:  # si alguna materia no tiene cupo
                    tiene_cupo = False
                    break  # no revisar más, esta combinacion no es válida
            
            # si no hay cupo disponible, saltar a la siguiente combinacion
            if not tiene_cupo:
                continue
            
            # SUB-PASO 4.2: actualizar cupos despues de asignar esta combinacion
            # crear nueva tupla de cupos con las materias asignadas decrementadas
            nuevos_cupos = list(cupos)  # convertir a lista para modificar
            for mat_idx, _ in combinacion:
                nuevos_cupos[mat_idx] = nuevos_cupos[mat_idx] - 1  # decrementar cupo
            # ejemplo: cupos=(2,1,1,1), combinacion=[(0,p1)] -> nuevos_cupos=(1,1,1,1)
            
            # SUB-PASO 4.3: convertir indices a codigos para calcular insatisfaccion
            # la funcion calcular_insatisfaccion_estudiante necesita codigos, no indices
            materias_asignadas = []  # -> [(101, 0.9), (103, 0.7)]
            for mat_idx, pref in combinacion:
                codigo = codigos[mat_idx]  # convertir indice -> codigo usando lista codigos
                materias_asignadas.append((codigo, pref))
            
            # SUB-PASO 4.4: calcular insatisfaccion del estudiante actual
            # fj = (1 - |asignadas|/|solicitadas|) * (Σ prioridades no asignadas / gamma)
            insatisfaccion = calcular_insatisfaccion_estudiante(
                materias_solicitadas,  # Códigos originales: [(101, 0.9), (102, 0.8)]
                materias_asignadas     # Códigos asignados: [(101, 0.9)]
            )
            
            # SUB-PASO 4.5: resolver recursivamente para los siguientes estudiantes
            # llamada recursiva: ¿cual es la solucion optima para estudiantes j+1...n?
            resto_asignaciones, resto_costo = dp(j + 1, tuple(nuevos_cupos))
            #                                      ↑              ↑
            #                              siguiente est.    cupos actualizados
            
            # costo total = insatisfacción del estudiante j + costo de j+1...n
            costo_total = insatisfaccion + resto_costo
            
            # SUB-PASO 4.6: actualizar si encontramos una mejor solucion
            # principio de optimalidad: elegir la combinacion que minimice costo total
            if costo_total < mejor_costo:
                mejor_costo = costo_total
                # guardar asignacion como estructura recursiva:
                # (materias_del_estudiante_j, (materias_del_j+1, (materias_del_j+2, ...)))
                mejor_asignacion = (tuple(materias_asignadas), resto_asignaciones)
        
        # PASO 5: guardar resultado en memoizacion antes de retornar
        resultado = (mejor_asignacion, mejor_costo)
        memo[clave] = resultado  # cache miss -> calcular y guardar
        return resultado
    
    # ejecutar programacion dinamica
    asignaciones_codificadas, costo_total = dp(0, cupos_iniciales)
    
    # decodificar resultado
    def decodificar(j, asignacion_codificada):
        if j == len(estudiantes):
            return []
        
        codigo_est = estudiantes[j][0]
        materias, resto = asignacion_codificada
        
        resultado = [(codigo_est, list(materias))]
        resultado_resto = decodificar(j + 1, resto)
        for item in resultado_resto:
            resultado.append(item)
        
        return resultado
    
    A = decodificar(0, asignaciones_codificadas)
    costo_normalizado = costo_total / r if r > 0 else 0.0
    
    return A, costo_normalizado