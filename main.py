import tkinter as tk
from tkinter import PhotoImage
from tkinter import scrolledtext, ttk
import os
from compilador_Julia.compilador_Julia import compilador_Julia
from compilador_Ruby.compilador_Ruby import compilador_Ruby

class VentanaPrincipal:

    def __init__(self, master):
        self.master = master
        self.master.title("Compilador Formales")
        self.master.state('zoomed')
        self.master.config(bg="black")
        self.crear_gui()

    def crear_gui(self):

    # Frame izquierdo
     frm_izq = tk.Frame(self.master, bg="black")
     frm_izq.grid(row=0, column=0, padx=10, pady=10, rowspan=5, sticky="nsew")

    # Frame derecho
     frm_der = tk.Frame(self.master, bg="black")
     frm_der.grid(row=0, column=1, padx=10, pady=10, rowspan=5, sticky="nsew")

    # Frame inferior
     frm_btn = tk.Frame(self.master, bg="black")
     frm_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Configuración de columnas y filas para que se expandan correctamente
     self.master.grid_rowconfigure(0, weight=1)
     self.master.grid_rowconfigure(1, weight=0)  # El peso es menor para que no expanda tanto el frame inferior
     self.master.grid_columnconfigure(0, weight=1)
     self.master.grid_columnconfigure(1, weight=1)

    # Contenido del frame izquierdo
     self.etq_codigo = tk.Label(frm_izq, text="Script", bg="black", fg="#00FF7F")
     self.etq_codigo.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

     self.cuadro_txt = scrolledtext.ScrolledText(frm_izq, wrap=tk.WORD, height=22, width=60)
     self.cuadro_txt.grid(row=1, column=0, padx=10, pady=5)

    # Contenido del frame derecho
     self.etq_ejecucion = tk.Label(frm_der, text="Ejecutar", bg="black", fg="#00FF7F")
     self.etq_ejecucion.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

     self.cuadro_ejecucion = scrolledtext.ScrolledText(frm_der, wrap=tk.WORD, height=18, width=95, state="disabled")
     self.cuadro_ejecucion.grid(row=1, column=0, padx=10, pady=(10, 5))

     self.btn_ejecutar = tk.Button(frm_der, text="Ejecutar", bg="#16770b", fg="white", height=3, width=20, command=self.compilar)
     self.btn_ejecutar.grid(row=2, column=0, padx=(0, 5), pady=10, sticky="w")

     self.btn_limpiar = tk.Button(frm_der, text="Borrar", bg="#FF0000", fg="white", height=3, width=20, command=self.limpiar)
     self.btn_limpiar.grid(row=2, column=0, padx=(5, 0), pady=10, sticky="e")

    # Contenido del frame inferior
     self.etq_automata = tk.Label(frm_btn, text="Automata de pila", bg="black", fg="#00FF7F")
     self.etq_automata.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

     self.tabla_automata = ttk.Treeview(frm_btn, columns=("Nombre", "Token", "Estado", "Regla"), show="headings")
     self.tabla_automata.heading("Nombre", text="Nombre")
     self.tabla_automata.heading("Token", text="Token")
     self.tabla_automata.heading("Estado", text="Estado")
     self.tabla_automata.heading("Regla", text="Regla")
     self.tabla_automata.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    # Ajustar el peso para las filas y columnas del frame inferior
     frm_btn.grid_rowconfigure(1, weight=1)
     frm_btn.grid_columnconfigure(0, weight=1)

    def limpiar(self):
        self.cuadro_txt.delete("1.0", tk.END)
        self.cuadro_ejecucion.config(state="normal")
        self.cuadro_ejecucion.delete("1.0", tk.END)
        self.cuadro_ejecucion.config(state="disabled")

        self.tabla_automata.delete(*self.tabla_automata.get_children())

    def compilar(self):

        comr = compilador_Ruby()
        comj = compilador_Julia()
        codigo = self.cuadro_txt.get("1.0", tk.END)

        with open('codigo.txt', 'w') as file:
            file.write(codigo)

        if self.detectar_lenguaje(codigo) == 'Julia':
            self.cuadro_ejecucion.config(state="normal")
            self.cuadro_ejecucion.delete("1.0", tk.END)
            self.compilar_julia()
            self.cuadro_ejecucion.config(state="disabled")

        elif self.detectar_lenguaje(codigo) == 'Ruby':
            self.cuadro_ejecucion.config(state="normal")
            self.cuadro_ejecucion.delete("1.0", tk.END)
            self.compilar_ruby()
            self.cuadro_ejecucion.config(state="disabled")

        else:
            self.cuadro_ejecucion.config(state="normal")
            self.cuadro_ejecucion.insert(tk.END, "No se reconoce el lenguaje del código ingresado.\n")
            self.cuadro_ejecucion.config(state="disabled")

    def detectar_lenguaje(self,codigo):
        # Palabras clave y constructos típicos de Julia
        palabras_clave_julia = ["julia>", "function", "end", "for", "while", "if", "elseif", "else", "return",
                                "break", "continue", "global", "const", "mutable", "struct", "module",
                                "using", "import", "=", "+=", "-=", ":", "1:", "#", "&&", "||", "==",
                                "!=", "<", ">", "<=", ">=", "->", "Int", "float64","Float64", "String",
                                "println", "sum", "sort","range", "sqrt", "div", "length", "get", "maximum", "minimum",
                                "rand", "findmin", "findmax", "cov", "element", "array", "dims", "julia"]

        # Palabras clave y constructos típicos de Ruby
        palabras_clave_ruby = ["def", "end", "if", "else", "elsif", "unless", "while", "until", "for",
                               "break", "next", "return", "module", "class", "begin", "rescue", "ensure",
                               "include", "require", "=", "+=", "-=", ":", "1..", "#", "&", "&&", "||", "==",
                               "!=", "<", ">", "<=", ">=", "->", "{", "}", "Integer", "Float", "String",
                               "puts", "sum", "sort", "group_by", "max", "min", "map", "empty?", "array", "new"]

        # Contadores para contar la cantidad de coincidencias con cada lenguaje
        contador_julia = 0
        contador_ruby = 0

        # Buscar coincidencias con palabras clave de Julia
        for palabra in palabras_clave_julia:
            if palabra in codigo:
                contador_julia += 1

        # Buscar coincidencias con palabras clave de Ruby
        for palabra in palabras_clave_ruby:
            if palabra in codigo:
                contador_ruby += 1

        # Determinar el lenguaje basado en los contadores
        if contador_julia > contador_ruby:
            return "Julia"
        elif contador_ruby > contador_julia:
            return "Ruby"
        else:
            return None

    def compilar_julia(self):
        comJ = compilador_Julia()
        codigo = self.cuadro_txt.get("1.0", tk.END)

        self.cuadro_ejecucion.config(state="normal")
        self.cuadro_ejecucion.delete("1.0", tk.END)

        # Mostrar "Julia" en el cuadro de ejecución
        self.cuadro_ejecucion.insert(tk.END, "Lenguaje Julia.\n")

        self.cuadro_ejecucion.insert(tk.END, self.detectar_formato_datos(codigo) + "\n")

        # Ejecutar el análisis del compilador_Julia
        for mensaje in comJ.analizador():
            self.cuadro_ejecucion.insert(tk.END, mensaje + "\n")

        self.cuadro_ejecucion.config(state="disabled")

        self.mostrar_datos_tabla(comJ.automata_Ruby())

    def compilar_ruby(self):
        comR = compilador_Ruby()
        codigo = self.cuadro_txt.get("1.0", tk.END)

        self.cuadro_ejecucion.config(state="normal")
        self.cuadro_ejecucion.delete("1.0", tk.END)

        # Mostrar "Ruby" en el cuadro de ejecución
        self.cuadro_ejecucion.insert(tk.END, "Lenguaje Ruby.\n")

        self.cuadro_ejecucion.insert(tk.END, self.detectar_formato_datos(codigo) + "\n")

        # Ejecutar el análisis del compilador_Ruby
        for mensaje in comR.analizadorR():
            self.cuadro_ejecucion.insert(tk.END, mensaje + "\n")

        self.cuadro_ejecucion.config(state="disabled")

        self.mostrar_datos_tabla(comR.automata_Ruby())

    def mostrar_datos_tabla(self, datos):
        self.tabla_automata.delete(*self.tabla_automata.get_children())
        for automata in datos:
            tipo_token, nombre_token, estado, regla = automata.split(", ")
            self.tabla_automata.insert("", "end", values=(tipo_token.split(": ")[1], nombre_token.split(": ")[1], estado.split(": ")[1], regla.split(": ")[1]))

    def detectar_formato_datos(self, codigo):
        formatos = {
           "sql": [ "SQL""SELECT ", "INSERT INTO ", "UPDATE ", "DELETE FROM ", "JOIN "],
           "xml": ["XML","<", ">"],
           "json": ["JSON","{", "}", "[", "]", ":"]
        }
        
        for palabra, descripcion in formatos.items():
            if palabra in codigo:
                return f"-->Se detectó formato de datos: {descripcion}"

        return "--> No se detectó ningún formato de datos XML, JSON o SQL."

def main():

    with open('codigo.txt', 'w') as file:
        file.write('')

    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()

if __name__ == '__main__':
    main()