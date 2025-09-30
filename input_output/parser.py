# Cargar datos desde un archivo .txt
def load_data_from_file(filename):
    with open(filename, 'r') as file:
        data = file.read().strip().splitlines()
    return data

# Interpretar y procesar los datos
# Recibe la data como una lista de strings
# Devuelve dos diccionarios: materias y estudiantes
def parse_data(data):
    # Tomar el primer valor de data como el número de asignaturas
    numero_de_asignaturas = int(data[0])

    # Inicializar diccionario para las materias
    materias = {}

    # Iterar sobre las siguientes lineas de data tomando en cuenta el número de asignaturas
    for i in range(1, numero_de_asignaturas + 1):
        # Dividir los valores separados por coma y convertirlos a enteros
        codigo, cupo = map(int, data[i].split(','))
        materias[codigo] = cupo
    
    # Tomar el siguiente valor como el número de estudiantes
    numero_de_estudiantes = int(data[numero_de_asignaturas + 1])

    # Inicializar diccionario para los estudiantes
    estudiantes = {}

    # Índice inicial para leer los datos de los estudiantes
    idx = numero_de_asignaturas + 2

    # Iterar sobre las siguientes lineas de data tomando en cuenta el número de estudiantes (cada estudiante tiene un bloque de información) 
    for i in range(numero_de_estudiantes):
        # Leer el código del estudiante y el número de materias que solicita
        codigo_estudiante, num_materias = map(int, data[idx].split(','))

        # Mover al siguiente índice para leer las materias solicitadas
        idx += 1

        # Inicializar lista para las solicitudes de las materias del estudiante
        solicitudes = []

        # Leer las materias solicitadas por el estudiante según el número de materias (numero de lineas del bloque)
        for j in range(num_materias):
            # Leer el código de la materia y la prioridad
            materia, prioridad = map(int, data[idx].split(','))
            # Agregar la solicitud a la lista
            solicitudes.append((materia, prioridad))
            # Mover al siguiente índice
            idx += 1

        # Agregar el estudiante y sus solicitudes de materias al diccionario
        estudiantes[codigo_estudiante] = solicitudes
    
    return materias, estudiantes