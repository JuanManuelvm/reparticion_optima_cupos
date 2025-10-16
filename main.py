import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from input_output.parser import getDataByTxt
from Voraz.rocV import rocV
from Dinamica.rocPD import rocPD
from FuerzaBruta.rocFB import rocFB
from input_output.salida import guardar_resultados 
import os
import time



class CuposGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Repartición Óptima de Cupos - Algoritmos Comparativos")
        self.root.geometry("1000x700")

        # Variables
        self.k = None
        self.r = None
        self.M = None
        self.E = None
        self.file_path = None

        # Variable del algoritmo seleccionado
        self.algoritmo_var = tk.StringVar(value="Dinamico")

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Títulos
        title_label = ttk.Label(main_frame, text="Repartición Óptima de Cupos", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10, sticky=tk.W)

        subtitle_label = ttk.Label(main_frame, text="Análisis de Algoritmos II - Comparación de Métodos", font=('Arial', 10))
        subtitle_label.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)

        # === FRAME DE CARGA DE ARCHIVO ===
        load_frame = ttk.LabelFrame(main_frame, text="Cargar Datos", padding="10")
        load_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        load_frame.columnconfigure(1, weight=1)

        self.load_button = ttk.Button(load_frame, text="Cargar Archivo .txt", command=self.load_file)
        self.load_button.grid(row=0, column=0, padx=(0, 10))

        self.file_label = ttk.Label(load_frame, text="No se ha cargado ningún archivo", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=tk.W)

        # === FRAME DE SELECCIÓN DE ALGORITMO ===
        algo_frame = ttk.LabelFrame(main_frame, text="Seleccionar Algoritmo", padding="10")
        algo_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Radiobutton(algo_frame, text="Fuerza Bruta", value="FuerzaBruta", variable=self.algoritmo_var).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(algo_frame, text="Voraz", value="Voraz", variable=self.algoritmo_var).grid(row=0, column=1, padx=10)
        ttk.Radiobutton(algo_frame, text="Dinámico", value="Dinamico", variable=self.algoritmo_var).grid(row=0, column=2, padx=10)

        ttk.Button(algo_frame, text="Ejecutar Algoritmo Seleccionado", command=self.run_algorithm).grid(row=0, column=3, padx=20)

        # === NOTEBOOK (pestañas) ===
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        self.resumen_frame = ttk.Frame(self.notebook, padding="10")
        self.materias_frame = ttk.Frame(self.notebook, padding="10")
        self.estudiantes_frame = ttk.Frame(self.notebook, padding="10")
        self.resultados_frame = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.resumen_frame, text="📊 Resumen")
        self.notebook.add(self.materias_frame, text="📚 Materias (M)")
        self.notebook.add(self.estudiantes_frame, text="👥 Estudiantes (E)")
        self.notebook.add(self.resultados_frame, text="⚙️ Resultados")

        self.setup_resumen_tab()
        self.setup_materias_tab()
        self.setup_estudiantes_tab()
        self.setup_resultados_tab()

    # ---------------------- PESTAÑAS ----------------------

    def setup_resumen_tab(self):
        self.resumen_text = scrolledtext.ScrolledText(self.resumen_frame, wrap=tk.WORD, height=20, font=('Courier', 10))
        self.resumen_text.pack(fill=tk.BOTH, expand=True)
        self.resumen_text.insert('1.0', "Carga un archivo para ver el resumen...")
        self.resumen_text.config(state=tk.DISABLED)

    def setup_materias_tab(self):
        tree_frame = ttk.Frame(self.materias_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.materias_tree = ttk.Treeview(tree_frame, columns=('Código', 'Cupo'), show='headings', yscrollcommand=scrollbar.set)
        self.materias_tree.heading('Código', text='Código Materia')
        self.materias_tree.heading('Cupo', text='Cupo Disponible')
        self.materias_tree.column('Código', width=200, anchor=tk.CENTER)
        self.materias_tree.column('Cupo', width=150, anchor=tk.CENTER)
        self.materias_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.materias_tree.yview)

    def setup_estudiantes_tab(self):
        self.estudiantes_text = scrolledtext.ScrolledText(self.estudiantes_frame, wrap=tk.WORD, font=('Courier', 9))
        self.estudiantes_text.pack(fill=tk.BOTH, expand=True)
        self.estudiantes_text.config(state=tk.DISABLED)

    def setup_resultados_tab(self):
        self.resultados_text = scrolledtext.ScrolledText(self.resultados_frame, wrap=tk.WORD, height=20, font=('Courier', 10))
        self.resultados_text.pack(fill=tk.BOTH, expand=True)
        self.resultados_text.insert('1.0', "Ejecuta un algoritmo para ver los resultados aquí.")
        self.resultados_text.config(state=tk.DISABLED)

    # ---------------------- FUNCIONES LÓGICAS ----------------------


    def load_file(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo de entrada",
                                               filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            try:
                self.k, self.r, self.M, self.E = getDataByTxt(file_path)
                self.file_path = file_path
                self.file_label.config(text=f"Archivo cargado: {os.path.basename(file_path)}", foreground="green")
                self.update_resumen()
                self.update_materias()
                self.update_estudiantes()
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.file_label.config(text="Error al cargar archivo", foreground="red")

    def run_algorithm(self):
        if not all([self.k, self.r, self.M, self.E]):
            messagebox.showwarning("Advertencia", "Primero carga un archivo antes de ejecutar un algoritmo.")
            return

        algoritmo = self.algoritmo_var.get()
        start = time.time()

        try:
            if algoritmo == "FuerzaBruta":
                # Convertir M y E a diccionarios
                materias_dict = {codigo: cupo for codigo, cupo in self.M}
                estudiantes_dict = {codigo_est: materias for codigo_est, materias in self.E}
                resultados, insat = rocFB(materias_dict, estudiantes_dict)

            elif algoritmo == "Voraz":
                # Convertir M y E a diccionarios
                materias_dict = {codigo: cupo for codigo, cupo in self.M}
                estudiantes_dict = {codigo_est: materias for codigo_est, materias in self.E}
                resultados, insat = rocV(materias_dict, estudiantes_dict)

            else:  # Dinámico
                resultados, insat = rocPD(self.k, self.r, self.M, self.E)

            elapsed = round(time.time() - start, 3)
            self.show_results(algoritmo, resultados, insat, elapsed)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar {algoritmo}:\n{e}")


    def show_results(self, algoritmo, resultados, insat, tiempo):
        """
        Muestra los resultados del algoritmo seleccionado en el panel de resultados.
        """
        self.resultados_text.config(state="normal")
        self.resultados_text.delete("1.0", tk.END)

        self.resultados_text.insert(tk.END, f"=== RESULTADOS {algoritmo.upper()} ===\n\n")

        # Mostrar asignaciones dependiendo del formato recibido
        if isinstance(resultados, dict):
            for est, materias in resultados.items():
                self.resultados_text.insert(tk.END, f"Estudiante {est}: {materias}\n")

        elif isinstance(resultados, list):
            for est, materias in resultados:
                codigos = [codigo for codigo, _ in materias]
                self.resultados_text.insert(tk.END, f"Estudiante {est}: {codigos}\n")

        self.resultados_text.insert(tk.END, "\n")
        self.resultados_text.insert(tk.END, f"Insatisfacción general: {insat:.4f}\n")
        self.resultados_text.insert(tk.END, f"Tiempo de ejecución: {tiempo:.3f} s\n")

        self.resultados_text.config(state="disabled")

        #  Guardar los resultados en txt automáticamente
        ruta_carpeta = "Resultados"
        nombre_archivo = f"resultado_{algoritmo.lower()}.txt"
        guardar_resultados(ruta_carpeta, nombre_archivo, resultados, insat)

        # Cambiar a la pestaña de resultados automáticamente
        self.notebook.select(self.resultados_frame)



    # ---------------------- ACTUALIZAR PESTAÑAS ----------------------

    def update_resumen(self):
        self.resumen_text.config(state=tk.NORMAL)
        self.resumen_text.delete('1.0', tk.END)
        resumen = f"""
{'='*60}
RESUMEN DE DATOS CARGADOS
{'='*60}
Total de Materias: {self.k}
Total de Estudiantes: {self.r}
Cupos totales: {sum(c for _, c in self.M)}
Promedio cupos/materia: {sum(c for _, c in self.M)/self.k:.2f}
Solicitudes totales: {sum(len(m) for _, m in self.E)}
Promedio materias/estudiante: {sum(len(m) for _, m in self.E)/self.r:.2f}
"""
        self.resumen_text.insert('1.0', resumen)
        self.resumen_text.config(state=tk.DISABLED)

    def update_materias(self):
        for item in self.materias_tree.get_children():
            self.materias_tree.delete(item)
        for codigo, cupo in self.M:
            self.materias_tree.insert('', tk.END, values=(codigo, cupo))

    def update_estudiantes(self):
        self.estudiantes_text.config(state=tk.NORMAL)
        self.estudiantes_text.delete('1.0', tk.END)
        for codigo_est, materias in self.E:
            self.estudiantes_text.insert(tk.END, f"Estudiante {codigo_est}:\n")
            for cod, p in materias:
                self.estudiantes_text.insert(tk.END, f"  - Materia {cod}, Prioridad {p}\n")
            self.estudiantes_text.insert(tk.END, "\n")
        self.estudiantes_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = CuposGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

