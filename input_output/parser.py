def calcular_gamma(num_materias):
        return 3 * num_materias - 1

def getDataByTxt(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    index = 0
    k = int(lines[index])
    index += 1

    M = []
    for _ in range(k):
        codigo, cupo = lines[index].split(',')
        M.append((int(codigo), int(cupo)))
        index += 1

    r = int(lines[index])
    index += 1

    E = []
    for _ in range(r):
        codigo_est, num_mats = lines[index].split(',')
        codigo_est = int(codigo_est)
        num_mats = int(num_mats)
        index += 1
        materias = []
        for _ in range(num_mats):
            cod_mat, prioridad = lines[index].split(',')
            materias.append((int(cod_mat), int(prioridad)))
            index += 1
        E.append((codigo_est, materias))

    # Validaciones
    for codigo_est, materias in E:
        suma_prioridades = sum(p for _, p in materias)
        gamma_value = calcular_gamma(len(materias))
        if suma_prioridades > gamma_value:
            raise ValueError(f"Estudiante {codigo_est}: suma de prioridades ({suma_prioridades}) excede γ({len(materias)})={gamma_value}")
        codigos = [c for c, _ in materias]
        if len(codigos) != len(set(codigos)):
            raise ValueError(f"Estudiante {codigo_est}: materias repetidas")

    return k, r, M, E