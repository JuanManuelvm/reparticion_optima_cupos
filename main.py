from input_output.parser import load_data_from_file, parse_data
from Voraz.rocV import rocV
from input_output.salida import calcularInsatisfaccionGeneral

def main():
    data = load_data_from_file('Pruebas/Prueba46.txt')
    materias, estudiantes = parse_data(data)
    #print(materias, estudiantes)
    materiasAsignadas = rocV(materias, estudiantes)
    print(materiasAsignadas)
    insatisfaccionGeneral = calcularInsatisfaccionGeneral(materiasAsignadas, estudiantes, materias)
    print(f'Insatisfacción General: {insatisfaccionGeneral}')

    #print(materiasAsignadas)
if __name__ == "__main__":
    # Run the main program
    main()