from input_output.parser import load_data_from_file, parse_data

def main():
    data = load_data_from_file('Pruebas/Prueba1.txt')
    materias, estudiantes = parse_data(data)
    print(materias, estudiantes)

if __name__ == "__main__":
    # Run the main program
    main()