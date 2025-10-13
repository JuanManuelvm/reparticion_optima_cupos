from input_output.parser import load_data_from_file, parse_data
from Voraz.rocV import rocV
from FuerzaBruta.rocFB import rocFB
from input_output.salida import calcularInsatisfaccionGeneral, guardar_resultados

def main():
    data = load_data_from_file('Pruebas/Prueba1.txt')
    materias, estudiantes = parse_data(data)
    #print(materias, estudiantes)

    satisfacion, solucion = rocFB(materias, estudiantes)
    guardar_resultados("Resultados/FBruta", "Resultado1.txt", solucion, satisfacion)
    print(f'Insatisfacción General: {satisfacion}')
    print(f'Solución: {solucion}')

    materiasAsignadas = rocV(materias, estudiantes)
    print(materiasAsignadas)
    insatisfaccionGeneral = calcularInsatisfaccionGeneral(materiasAsignadas, estudiantes, materias)
    print(f'Insatisfacción General: {insatisfaccionGeneral}')

    #print(materiasAsignadas)
if __name__ == "__main__":
    # Run the main program
    main()