import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from input_output.parser import load_data_from_file, parse_data
from Voraz.rocV import rocV
from FuerzaBruta.rocFB import rocFB
from input_output.salida import calcularInsatisfaccionGeneral, guardar_resultados
import os
import time

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Asignación de Materias - Interfaz de Ejecución")
        self.root.geometry("900x700")  # Ajustada altura para nuevo botón
        self.root.config(bg="#f7f7f7")

        # Variables
        self.file_path = tk.StringVar()
        self.file_name = ""

        # Título principal
        tk.Label(root, text="Sistema de Asignación de Materias", 
                 font=("Arial", 18, "bold"), bg="#f7f7f7").pack(pady=15)

        # Sección para cargar archivo
        frame_file = tk.Frame(root, bg="#f7f7f7")
        frame_file.pack(pady=10)
        tk.Label(frame_file, text="Archivo de entrada (.txt):", bg="#f7f7f7", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_file, textvariable=self.file_path, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_file, text="Examinar", command=self.cargar_archivo, bg="#d9d9d9").pack(side=tk.LEFT)

        # Botones de ejecución
        frame_buttons = tk.Frame(root, bg="#f7f7f7")
        frame_buttons.pack(pady=20)
        tk.Button(frame_buttons, text="Ejecutar Fuerza Bruta", command=self.ejecutar_fb, bg="#ffcccc", width=25).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Ejecutar Algoritmo Voraz", command=self.ejecutar_voraz, bg="#ccffcc", width=25).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_buttons, text="Ejecutar Algoritmo Dinámico", command=self.ejecutar_dinamico_placeholder, bg="#ccccff", width=25).pack(side=tk.LEFT, padx=10)

        # Sección de visualización
        tk.Label(root, text="Entradas / Salidas:", bg="#f7f7f7", font=("Arial", 13, "bold")).pack(pady=5)
        self.text_output = scrolledtext.ScrolledText(root, width=100, height=25, wrap=tk.WORD, bg="#ffffff", font=("Consolas", 10))
        self.text_output.pack(padx=10, pady=5)

    # ---------------- FUNCIONES ----------------

    def cargar_archivo(self):
        """Permite seleccionar un archivo de texto y mostrar su contenido."""
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            self.file_path.set(path)
            self.file_name = os.path.splitext(os.path.basename(path))[0]
            try:
                with open(path, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, f"=== ARCHIVO CARGADO: {path} ===\n\n")
                self.text_output.insert(tk.END, contenido)
                self.text_output.insert(tk.END, "\n\n=== FIN DE ENTRADA ===\n\n")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def ejecutar_fb(self):
        """Ejecuta el algoritmo de Fuerza Bruta, muestra y guarda resultados."""
        try:
            if not self.file_path.get():
                messagebox.showwarning("Advertencia", "Primero selecciona un archivo de entrada.")
                return

            start = time.time()
            data = load_data_from_file(self.file_path.get())
            materias, estudiantes = parse_data(data)
            insatisfaccion, solucion = rocFB(materias, estudiantes)
            elapsed = round(time.time() - start, 3)

            # Guardar resultados con el nombre de la prueba
            out_dir = "Resultados/FBruta"
            os.makedirs(out_dir, exist_ok=True)
            output_filename = f"Resultado_{self.file_name}_FB.txt"
            guardar_resultados(out_dir, output_filename, solucion, insatisfaccion)

            # Mostrar en interfaz
            self.text_output.insert(tk.END, f"\n=== RESULTADOS FUERZA BRUTA ({self.file_name}) ===\n")
            self.text_output.insert(tk.END, f"Insatisfacción General: {insatisfaccion}\n")
            self.text_output.insert(tk.END, f"Solución: {solucion}\n")
            self.text_output.insert(tk.END, f"Tiempo de ejecución: {elapsed} segundos\n")
            self.text_output.insert(tk.END, f"Resultado guardado en: {out_dir}/{output_filename}\n\n")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en Fuerza Bruta:\n{e}")

    def ejecutar_voraz(self):
        """Ejecuta el algoritmo voraz, muestra y guarda resultados."""
        try:
            if not self.file_path.get():
                messagebox.showwarning("Advertencia", "Primero selecciona un archivo de entrada.")
                return

            start = time.time()
            data = load_data_from_file(self.file_path.get())
            materias, estudiantes = parse_data(data)
            materiasAsignadas, insatisfaccion = rocV(materias, estudiantes)
            insatisfaccion2 = calcularInsatisfaccionGeneral(materiasAsignadas, estudiantes, materias)
            print(insatisfaccion)
            print(insatisfaccion2)
            elapsed = round(time.time() - start, 3)

            # Guardar resultados con el mismo formato y nombre de la prueba
            out_dir = "Resultados/Voraz"
            os.makedirs(out_dir, exist_ok=True)
            output_filename = f"Resultado_{self.file_name}_Voraz.txt"
            guardar_resultados(out_dir, output_filename, materiasAsignadas, insatisfaccion)

            # Mostrar en interfaz
            self.text_output.insert(tk.END, f"\n=== RESULTADOS ALGORITMO VORAZ ({self.file_name}) ===\n")
            self.text_output.insert(tk.END, f"Insatisfacción General: {insatisfaccion}\n")
            self.text_output.insert(tk.END, f"Materias Asignadas: {materiasAsignadas}\n")    
            self.text_output.insert(tk.END, f"Tiempo de ejecución: {elapsed} segundos\n")
            self.text_output.insert(tk.END, f"Resultado guardado en: {out_dir}/{output_filename}\n\n")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error en el Algoritmo Voraz:\n{e}")

    def ejecutar_dinamico_placeholder(self):
        """Espacio reservado para el algoritmo dinámico."""
        messagebox.showinfo("Dinámico", "La funcionalidad del algoritmo dinámico será añadida próximamente.")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
