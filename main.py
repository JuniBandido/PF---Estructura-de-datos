import tkinter as tk

COLORES = {
    "fondo": "#F4F9FD",
    "encabezado": "#1565C0",
    "texto_encabezado": "#FFFFFF",
    "subtexto": "#90CAF9",

    "barra_lateral": "#FFFFFF",
    "barra_info": "#E3F2FD",
    "canvas": "#F4F9FD",
    "separador": "#BBDEFB"
}


class FlowTreeUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("FlowTree")
        self.geometry("1200x700")
        self.configure(bg=COLORES["fondo"])

        self.construir_ui()

    def construir_ui(self):
        encabezado = tk.Frame(self,bg=COLORES["encabezado"],height=60)
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        titulo = tk.Label(encabezado,text="FlowTree",bg=COLORES["encabezado"],fg=COLORES["texto_encabezado"],font=("Segoe UI", 18, "bold"))
        titulo.pack(side="left", padx=20)

        subtitulo = tk.Label(encabezado,text="Visualizador de Árboles",bg=COLORES["encabezado"],fg=COLORES["subtexto"],font=("Segoe UI", 10))
        subtitulo.pack(side="left")

        contenedor = tk.Frame(self,bg=COLORES["fondo"])
        contenedor.pack(fill="both", expand=True)

        barra_lateral = tk.Frame(contenedor,bg=COLORES["barra_lateral"],width=280)

        barra_lateral.pack(side="left", fill="y")
        barra_lateral.pack_propagate(False)

        linea = tk.Frame(contenedor,bg=COLORES["separador"],width=1)
        linea.pack(side="left", fill="y")

        panel_derecho = tk.Frame(contenedor,bg=COLORES["fondo"])
        panel_derecho.pack(side="left", fill="both", expand=True)

        barra_info = tk.Frame(panel_derecho,bg=COLORES["barra_info"],height=40)

        barra_info.pack(fill="x")
        barra_info.pack_propagate(False)

        etiqueta_altura = tk.Label(barra_info,text="Altura: -",bg=COLORES["barra_info"],font=("Segoe UI", 10, "bold"))
        etiqueta_altura.pack(side="left", padx=20)

        etiqueta_nodos = tk.Label(barra_info,text="Nodos: -",bg=COLORES["barra_info"],font=("Segoe UI", 10, "bold"))
        etiqueta_nodos.pack(side="left", padx=20)

        etiqueta_raiz = tk.Label(barra_info,text="Raíz: -",bg=COLORES["barra_info"],font=("Segoe UI", 10, "bold"))
        etiqueta_raiz.pack(side="left", padx=20)

        self.canvas_arbol = tk.Canvas(panel_derecho,bg=COLORES["canvas"],highlightthickness=0)
        self.canvas_arbol.pack(fill="both",expand=True,padx=10,pady=10)


if __name__ == "__main__":

    app = FlowTreeUI()
    app.mainloop()