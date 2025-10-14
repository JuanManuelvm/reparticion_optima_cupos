# logica.py
# ========================================
# Contiene TODA la lógica de cálculo, lectura de archivos y validaciones
# ========================================

from itertools import combinations
from functools import lru_cache




def getDataByTxt(file_path):
    """Lee un archivo de texto y retorna k, r, M, E parseados según el formato especificado."""
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    
    index = 0
    
    # Leer k (número de materias)
    k = int(lines[index])
    index += 1
    
    # Leer materias M
    M = []
    for i in range(k):
        codigo, cupo = lines[index].split(',')
        M.append((int(codigo), int(cupo)))
        index += 1
    
    # Leer r (número de estudiantes)
    r = int(lines[index])
    index += 1
    
    # Leer estudiantes E
    E = []
    for j in range(r):
        codigo_estudiante, num_materias = lines[index].split(',')
        codigo_estudiante = int(codigo_estudiante)
        num_materias = int(num_materias)
        index += 1
        
        materias_solicitadas = []
        for l in range(num_materias):
            codigo_materia, prioridad = lines[index].split(',')
            materias_solicitadas.append((int(codigo_materia), int(prioridad)))
            index += 1
        
        E.append((codigo_estudiante, materias_solicitadas))
    
    # Validar restricciones
    for codigo_est, materias in E:
        suma_prioridades = sum(prioridad for _, prioridad in materias)
        gamma_value = calcular_gamma(len(materias))
        
        if suma_prioridades > gamma_value:
            raise ValueError(
                f"Estudiante {codigo_est}: suma de prioridades ({suma_prioridades}) "
                f"excede γ({len(materias)}) = {gamma_value}"
            )
        
        codigos_materias = [codigo for codigo, _ in materias]
        if len(codigos_materias) != len(set(codigos_materias)):
            raise ValueError(f"Estudiante {codigo_est}: tiene materias repetidas")
    
    return k, r, M, E


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





def rocPD_lru(k, r, M, E):
    """
    k (int)  : numero de materias disponibles
    r (int)  : numero de estudiantes
    M (list) : lista de tuplas (codigo_materia, cupo)
    E (list) : lista de tuplas (codigo_estudiante, [(codigo_materia, prioridad), ...])
    """
    
    # Crear mapeo de códigos a índices para representación compacta
    codigos_materias = sorted([codigo for codigo, _ in M])
    codigo_a_idx = {codigo: i for i, codigo in enumerate(codigos_materias)}
    idx_a_codigo = {i: codigo for codigo, i in codigo_a_idx.items()}
    
    # Cupos iniciales como tupla (inmutable y hasheable)
    cupos_iniciales = tuple(cupo for _, cupo in sorted(M, key=lambda x: x[0]))
    
    # Pre-procesar estudiantes: convertir códigos a índices
    estudiantes_procesados = []
    for codigo_est, materias_solicitadas in E:
        materias_idx = [(codigo_a_idx[codigo], pref) 
                        for codigo, pref in materias_solicitadas]
        estudiantes_procesados.append((codigo_est, materias_idx, materias_solicitadas))
    
    # Pre-calcular todas las combinaciones posibles para cada estudiante
    combinaciones_por_estudiante = []
    for _, materias_idx, _ in estudiantes_procesados:
        combos = []
        for size in range(len(materias_idx) + 1):
            for comb in combinations(materias_idx, size):
                combos.append(list(comb))
        combinaciones_por_estudiante.append(combos)
    
    @lru_cache(maxsize=None)
    def dp(j, cupos_tuple):
        """
        Calcula la mínima insatisfacción para estudiantes desde j hasta el final.
        
        Args:
            j: índice del estudiante actual
            cupos_tuple: tupla con cupos restantes (inmutable)
        
        Returns:
            (mejor_asignacion_codificada, mejor_costo)
        """
        if j == len(estudiantes_procesados):
            return [], 0.0
        
        codigo_est, materias_idx, materias_solicitadas = estudiantes_procesados[j]
        mejor_costo = float("inf")
        mejor_asignacion = None
        
        # Probar todas las combinaciones pre-calculadas
        for maj_idx in combinaciones_por_estudiante[j]:
            # Verificar disponibilidad de cupos
            valido = all(cupos_tuple[mat_idx] > 0 for mat_idx, _ in maj_idx)
            
            if not valido:
                continue
            
            # Actualizar cupos (crear nueva tupla)
            nuevos_cupos = list(cupos_tuple)
            for mat_idx, _ in maj_idx:
                nuevos_cupos[mat_idx] -= 1
            nuevos_cupos_tuple = tuple(nuevos_cupos)
            
            # Convertir asignación de índices a códigos para calcular insatisfacción
            maj_codigos = [(idx_a_codigo[mat_idx], pref) for mat_idx, pref in maj_idx]
            
            # Calcular insatisfacción del estudiante actual usando la función original
            fj = calcular_insatisfaccion_estudiante(materias_solicitadas, maj_codigos)
            
            # Resolver recursivamente
            asig_restante, costo_restante = dp(j + 1, nuevos_cupos_tuple)
            costo_total = fj + costo_restante
            
            if costo_total < mejor_costo:
                mejor_costo = costo_total
                # Guardar asignación como tupla de códigos (para decodificar después)
                mejor_asignacion = (tuple(maj_codigos), asig_restante)
        
        return mejor_asignacion, mejor_costo
    
    # Ejecutar DP
    asignacion_codificada, costo_total = dp(0, cupos_iniciales)
    
    # Decodificar la asignación
    def decodificar_asignacion(j, asig_cod):
        """Convierte la asignación codificada a formato legible."""
        if j == len(estudiantes_procesados):
            return []
        
        codigo_est = estudiantes_procesados[j][0]
        materias_asignadas, resto = asig_cod
        
        resultado = [(codigo_est, list(materias_asignadas))]
        resultado.extend(decodificar_asignacion(j + 1, resto))
        return resultado
    
    A = decodificar_asignacion(0, asignacion_codificada)
    
    # Normalizar el costo
    costo_normalizado = costo_total / r if r > 0 else 0.0
    
    # Estadísticas de memoización
    info = dp.cache_info()
    
    
    print(f"\nInsatisfacción general mínima: {costo_normalizado:.4f}")

    return A, costo_normalizado




def rocPD(k, r, M, E):
    """
    Algoritmo de Programación Dinámica con memoización MANUAL para asignar materias.
    
    Parámetros:
    - k: número de materias disponibles
    - r: número de estudiantes
    - M: lista de (codigo_materia, cupo)
    - E: lista de (codigo_estudiante, [(codigo_materia, prioridad), ...])
    
    Retorna:
    - A: asignaciones óptimas
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
    


    # Se organizan los cupos en una tupla de manera que queden con el mismo orden que los codigos para que esten sincronizados
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
    # FASE 2: PROGRAMACIÓN DINÁMICA CON MEMOIZACIÓN
    # ============================================================================
    
    # Diccionario para memoización: guarda resultados de estados ya calculados
    # Clave: (j, cupos) donde j es índice de estudiante y cupos es tupla de cupos restantes
    # Valor: (mejor_asignacion, mejor_costo) solución óptima para ese estado
    memo = {}  # -> {(0, (2,1,1,1)): ([...], 1.5), (1, (1,0,1,1)): ([...], 0.8), ...}
    
    # Función recursiva con memoización
    def dp(j, cupos):
        """
        Función recursiva que implementa programación dinámica con memoización.
        
        Resuelve el subproblema: ¿Cuál es la asignación óptima para los estudiantes
        desde j hasta el final, dado que tenemos 'cupos' disponibles?
        
        Parámetros:
        - j: índice del estudiante actual (de 0 a len(estudiantes)-1)
        - cupos: tupla con cupos restantes de cada materia (índice i = materia i)

                Ejemplo: (2, 1, 0, 3) significa mat[0]=2 cupos, mat[1]=1, mat[2]=0, mat[3]=3
        
        Retorna:
        - (mejor_asignacion, mejor_costo): tupla con la asignación óptima y su costo
        mejor_asignacion: estructura recursiva ((materias_est_j, resto_asignaciones))
        mejor_costo: float con la insatisfacción total acumulada
        
        Estado del DP:
        - Espacio de estados: (j, cupos) con j ∈ [0, n] y cupos ∈ ∏[0, Ci]
        - Subestructura óptima: solución óptima de (j, cupos) se construye de (j+1, cupos_actualizados)
        - Solapamiento: el mismo estado (j, cupos) puede alcanzarse por múltiples caminos
        """
        
        # PASO 1: Verificar memoización
        # Crear clave única para el estado actual (j, cupos)
        clave = (j, cupos)
        
        # Si ya calculamos este estado antes, devolver resultado guardado (cache hit)
        if clave in memo:
            return memo[clave]  # O(1) - evita recalcular
        
        # PASO 2: Caso base
        # Si ya procesamos todos los estudiantes, no hay más insatisfacción que agregar
        if j == len(estudiantes):
            resultado = ([], 0.0)  # (asignaciones_vacías, costo_cero)
            memo[clave] = resultado  # Guardar en memo
            return resultado
        
        # PASO 3: Caso recursivo
        # Obtener información del estudiante actual
        codigo_est, materias_idx, materias_solicitadas = estudiantes[j]
        #            ↑               ↑
        #            índices         códigos originales
        
        # Inicializar búsqueda de la mejor opción
        mejor_costo = float("inf")  # Empezar con costo infinito
        mejor_asignacion = None     # No hay asignación aún
        
        # PASO 4: Explorar todas las combinaciones posibles para el estudiante j
        # combinaciones[j] = [[], [(0,p1)], [(1,p2)], [(0,p1),(1,p2)], ...]
        for combinacion in combinaciones[j]:
            # combinacion es una posible asignación: ej. [(0, 0.9), (2, 0.7)]
            #                                              ↑         ↑
            #                                          índice_mat  prioridad
            
            # SUB-PASO 4.1: Verificar disponibilidad de cupos
            # Revisar que TODAS las materias en la combinación tengan cupo > 0
            tiene_cupo = True
            for mat_idx, _ in combinacion:
                if cupos[mat_idx] <= 0:  # Si alguna materia no tiene cupo
                    tiene_cupo = False
                    break  # No revisar más, esta combinación no es válida
            
            # Si no hay cupo disponible, saltar a la siguiente combinación
            if not tiene_cupo:
                continue
            
            # SUB-PASO 4.2: Actualizar cupos después de asignar esta combinación
            # Crear nueva tupla de cupos con las materias asignadas decrementadas
            nuevos_cupos = list(cupos)  # Convertir a lista para modificar
            for mat_idx, _ in combinacion:
                nuevos_cupos[mat_idx] = nuevos_cupos[mat_idx] - 1  # Decrementar cupo
            # Ejemplo: cupos=(2,1,1,1), combinacion=[(0,p1)] → nuevos_cupos=(1,1,1,1)
            
            # SUB-PASO 4.3: Convertir índices a códigos para calcular insatisfacción
            # La función calcular_insatisfaccion_estudiante necesita códigos, no índices
            materias_asignadas = []  # -> [(101, 0.9), (103, 0.7)]
            for mat_idx, pref in combinacion:
                codigo = codigos[mat_idx]  # Convertir índice → código usando lista codigos
                materias_asignadas.append((codigo, pref))
            
            # SUB-PASO 4.4: Calcular insatisfacción del estudiante actual
            # fj = (1 - |asignadas|/|solicitadas|) * (Σ prioridades no asignadas / gamma)
            insatisfaccion = calcular_insatisfaccion_estudiante(
                materias_solicitadas,  # Códigos originales: [(101, 0.9), (102, 0.8)]
                materias_asignadas     # Códigos asignados: [(101, 0.9)]
            )
            
            # SUB-PASO 4.5: Resolver recursivamente para los siguientes estudiantes
            # Llamada recursiva: ¿cuál es la solución óptima para estudiantes j+1...n?
            resto_asignaciones, resto_costo = dp(j + 1, tuple(nuevos_cupos))
            #                                      ↑              ↑
            #                              siguiente est.    cupos actualizados
            
            # Costo total = insatisfacción del estudiante j + costo de j+1...n
            costo_total = insatisfaccion + resto_costo
            
            # SUB-PASO 4.6: Actualizar si encontramos una mejor solución
            # Principio de optimalidad: elegir la combinación que minimice costo total
            if costo_total < mejor_costo:
                mejor_costo = costo_total
                # Guardar asignación como estructura recursiva:
                # (materias_del_estudiante_j, (materias_del_j+1, (materias_del_j+2, ...)))
                mejor_asignacion = (tuple(materias_asignadas), resto_asignaciones)
        
        # PASO 5: Guardar resultado en memoización antes de retornar
        resultado = (mejor_asignacion, mejor_costo)
        memo[clave] = resultado  # Cache miss → calcular y guardar
        return resultado
    
    # Ejecutar programación dinámica
    asignaciones_codificadas, costo_total = dp(0, cupos_iniciales)
    
    # Decodificar resultado
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
    
    # Estadísticas de memoización
    print(f"\nEstadísticas de memoización:")
    #print(f"  Estados únicos calculados: {len(memo)}")
    print("\nRESULTADO FINAL:")
    print("-" * 70)
    print("Asignaciones óptimas (A):")
    for est, materias in A:
        print(f"  Estudiante {est}: {[codigo for codigo, _ in materias]}")
    print(f"  Insatisfacción general mínima: {costo_normalizado:.4f}")
    
    return A, costo_normalizado