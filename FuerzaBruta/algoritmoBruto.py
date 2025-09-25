#Debe ir el algoritmo Bruto
import io

def LecturaDatos(prueba):
    #Leer datos del archivo
    entrada = io.open("../prueba1.txt", "r")
    datos = entrada.readlines()
    entrada.close()

    # 1. Extraer número de materias
    k = int(datos[0][0])

    # 2. Procesar materias
    M = []
    for i in range(1, k+1):
        codigo, cupo = datos[i].strip().split(",")
        M.append((codigo, int(cupo)))

    # 3. Número de estudiantes
    r = int(datos[k+1].strip())

    # 4. Procesar estudiantes
    E = []
    idx = k+2
    for _ in range(r):
        est, n_mats = datos[idx].strip().split(",")
        n_mats = int(n_mats)
        idx += 1
        ms = []
        for _ in range(n_mats):
            mat, pri = datos[idx].strip().split(",")
            ms.append((mat, int(pri)))
            idx += 1
        E.append((est, ms))
    return M, E

# Algoritmo de fuerza bruta
# Restriccion #1: La suma de las prioridades de todas 
#                 las materias de un estudiante debe ser menor o igual a len(E[i][1]).
# Restriccion #2: El estudiante no puede pedir materias repetidas.
def algoritmoBruto(M, E):
    A = []
    for i in range(len(E)):
        est, ms = E[i]
        asignadas = []
        prioridades = [pri for _, pri in ms]

        if sum(prioridades) <= len(ms)+1:
            codigos_vistos = []
            for mat, pri in ms:
                if mat not in codigos_vistos:
                    codigos_vistos.append(mat)
                    for codigo, cupo in M:
                        if mat == codigo and cupo > 0:
                            asignadas.append(mat)
                            M = [(c, cupo-1) if c == codigo else (c, cupo) for c, cupo in M]                            
        A.append((est, asignadas))
    return A

#Principal
path = "../prueba1.txt"
M, E = LecturaDatos(path)
A = algoritmoBruto(M, E)
print("Asignaciones:", A)
print(M)
print(E)

