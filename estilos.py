# ===== COLORES =====
COLOR_FONDO = "#ecf0f1"
COLOR_TEXTO = "#2c3e50"
COLOR_BOTON = "#3498db"
COLOR_BOTON_TEXTO = "#ffffff"

# ===== FUENTES =====
FUENTE_TITULO = ("Arial", 16, "bold")
FUENTE_TEXTO = ("Arial", 11)
FUENTE_BOTON = ("Arial", 11, "bold")

# ===== FUNCIONES OPCIONALES =====
def aplicar_fondo(ventana):
    ventana.configure(bg=COLOR_FONDO)

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()  # asegura medidas correctas

    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")